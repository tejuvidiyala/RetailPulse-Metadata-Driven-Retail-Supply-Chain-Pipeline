import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import pandas as pd
from datetime import datetime
from utils import load_config, setup_logger, get_db_connection, save_to_sql, init_spark_session
def run_gold_layer():
    config = load_config()
    logger = setup_logger()
    
    logger.info("Starting Gold Layer KPI Aggregations...")
    
    gold_config = config['layers']['gold']
    silver_dir = gold_config['source_dir']
    target_dir = gold_config['target_dir']
    engine_choice = config['pipeline'].get('engine', 'pandas').lower()
    
    # Adjust paths if running from scripts directory
    if not os.path.exists(silver_dir) and os.path.exists(os.path.join("..", silver_dir)):
        silver_dir = os.path.join("..", silver_dir)
        target_dir = os.path.join("..", target_dir)
        
    os.makedirs(target_dir, exist_ok=True)
    
    # Define standard SQL queries for KPIs
    # These queries run identically on SQLite and PySpark Temp Views!
    kpi_queries = {
        "low_stock_alerts": """
            SELECT p.product_name, p.category, s.store_name, s.city, i.stock_level, i.reorder_level, 
                   (i.reorder_level - i.stock_level) as units_needed
            FROM silver_inventory i
            JOIN silver_products p ON i.product_id = p.product_id
            JOIN silver_stores s ON i.store_id = s.store_id
            WHERE i.low_stock_flag = 1 OR i.low_stock_flag = 'true'
        """,
        "daily_sales": """
            SELECT order_date as date, count(order_id) as total_orders, sum(total_value) as total_revenue, 
                   avg(total_value) as avg_order_val
            FROM silver_orders
            GROUP BY order_date
            ORDER BY date ASC
        """,
        "top_products": """
            SELECT p.product_name, p.category, sum(o.total_value) as total_revenue, sum(o.quantity) as units_sold
            FROM silver_orders o
            JOIN silver_products p ON o.product_id = p.product_id
            GROUP BY p.product_name, p.category
            ORDER BY total_revenue DESC
            LIMIT 10
        """,
        "store_performance": """
            SELECT s.store_name, s.city, s.region, count(o.order_id) as total_orders, sum(o.total_value) as total_revenue
            FROM silver_orders o
            JOIN silver_stores s ON o.store_id = s.store_id
            GROUP BY s.store_name, s.city, s.region
            ORDER BY total_revenue DESC
        """,
        "category_revenue": """
            SELECT p.category, sum(o.total_value) as total_revenue, sum(o.quantity) as units_sold
            FROM silver_orders o
            JOIN silver_products p ON o.product_id = p.product_id
            GROUP BY p.category
            ORDER BY total_revenue DESC
        """
    }
    
    gold_metrics = {}
    db_conn = get_db_connection()
    spark = None
    
    # 1. Initialize PySpark session if Spark engine is requested
    if engine_choice == 'spark':
        logger.info("Initializing PySpark Session for Gold layer computations...")
        spark = init_spark_session()
        if spark:
            logger.info("PySpark initialized successfully! Running with Spark SQL engine.")
            # Load Silver tables into PySpark DataFrames and create views
            for dataset in ["orders", "inventory", "products", "stores", "suppliers"]:
                csv_path = os.path.join(silver_dir, f"{dataset}_clean.csv")
                if os.path.exists(csv_path):
                    sdf = spark.read.csv(csv_path, header=True, inferSchema=True)
                    sdf.createOrReplaceTempView(f"silver_{dataset}")
                else:
                    logger.error(f"Silver table file not found for Spark: {csv_path}")
        else:
            logger.warning("Failed to initialize PySpark Session. Falling back to SQLite SQL engine.")
            engine_choice = 'pandas'
            
    # 2. Execute KPI computations using the selected engine
    for kpi_name, query in kpi_queries.items():
        output_file = gold_config['kpis'][kpi_name]['output_file']
        dest_path = os.path.join(target_dir, output_file)
        
        logger.info(f"Computing KPI '{kpi_name}' using '{engine_choice.upper()}' engine...")
        
        try:
            if engine_choice == 'spark' and spark:
                # Run query in Spark
                spark_df = spark.sql(query)
                # Convert back to Pandas for CSV write & local database sync
                df = spark_df.toPandas()
            else:
                # Run query in SQLite
                df = pd.read_sql_query(query, db_conn)
                
            # Post-processing: rounding values for clean reporting
            if 'total_revenue' in df.columns:
                df['total_revenue'] = df['total_revenue'].round(2)
            if 'avg_order_val' in df.columns:
                df['avg_order_val'] = df['avg_order_val'].round(2)
                
            # Save to Gold layer as CSV
            df.to_csv(dest_path, index=False)
            logger.info(f"Gold KPI Success: '{kpi_name}' -> Saved to '{dest_path}' ({len(df)} rows)")
            
            # Sync back to SQLite Database under 'gold_' prefix
            save_to_sql(df, f"gold_{kpi_name}", db_conn)
            
            gold_metrics[kpi_name] = {
                "rows": len(df),
                "columns": list(df.columns),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to compute KPI '{kpi_name}' with {engine_choice.upper()}: {str(e)}")
            db_conn.close()
            if spark:
                spark.stop()
            raise e
            
    db_conn.close()
    if spark:
        spark.stop()
        logger.info("Spark Session stopped successfully.")
        
    # Save gold metadata
    metrics_path = os.path.join(target_dir, "gold_metadata.json")
    with open(metrics_path, 'w') as f:
        json.dump(gold_metrics, f, indent=4)
        
    logger.info(f"Gold layer processing complete. Metadata saved to {metrics_path}")
    return gold_metrics
if __name__ == "__main__":
    run_gold_layer()
