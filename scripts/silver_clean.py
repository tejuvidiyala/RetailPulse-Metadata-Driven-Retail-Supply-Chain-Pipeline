import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from datetime import datetime
from utils import load_config, setup_logger, get_db_connection, save_to_sql
def run_silver_layer():
    config = load_config()
    logger = setup_logger()
    
    logger.info("Starting Silver Layer Processing...")
    
    silver_config = config['layers']['silver']
    source_dir = silver_config['source_dir']
    target_dir = silver_config['target_dir']
    engine = config['pipeline']['engine']
    
    # Adjust paths if running from scripts directory
    if not os.path.exists(source_dir) and os.path.exists(os.path.join("..", source_dir)):
        source_dir = os.path.join("..", source_dir)
        target_dir = os.path.join("..", target_dir)
        
    os.makedirs(target_dir, exist_ok=True)
    
    # Connect to SQLite for SQL support
    db_conn = get_db_connection()
    
    silver_metrics = {}
    
    # Process each dataset based on metadata rules
    for dataset_name, dataset_meta in silver_config['datasets'].items():
        logger.info(f"Processing dataset '{dataset_name}' for Silver Layer...")
        
        src_path = os.path.join(source_dir, f"{dataset_name}.csv")
        dest_path = os.path.join(target_dir, f"{dataset_name}_clean.csv")
        
        if not os.path.exists(src_path):
            logger.error(f"Bronze file not found: {src_path}")
            raise FileNotFoundError(f"Bronze file not found for dataset {dataset_name}")
            
        try:
            # 1. Load Data
            df = pd.read_csv(src_path)
            raw_rows = len(df)
            
            # 2. Enforce schema/types defined in metadata config
            cols_meta = dataset_meta['columns']
            for col, col_type in cols_meta.items():
                if col in df.columns:
                    if col_type == 'integer':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                    elif col_type == 'float':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype(float)
                    elif col_type == 'date':
                        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    elif col_type == 'string':
                        df[col] = df[col].astype(str)
            
            # 3. Clean nulls based on metadata rules
            rules = dataset_meta.get('rules', {})
            remove_null_cols = rules.get('remove_nulls', [])
            if remove_null_cols:
                df = df.dropna(subset=[c for c in remove_null_cols if c in df.columns])
            
            # 4. Remove duplicates based on metadata rules
            if rules.get('remove_duplicates', False):
                dup_keys = rules.get('duplicate_keys', [])
                if dup_keys:
                    df = df.drop_duplicates(subset=[k for k in dup_keys if k in df.columns])
                else:
                    df = df.drop_duplicates()
            
            # 5. Enrichments
            enrichments = dataset_meta.get('enrichment', [])
            for enrich in enrichments:
                col_name = enrich['column']
                expr = enrich['expression']
                
                # Metadata evaluation of enrichment expressions
                if expr == "quantity * price" and 'quantity' in df.columns and 'price' in df.columns:
                    df[col_name] = df['quantity'] * df['price']
                elif expr == "stock_level < reorder_level" and 'stock_level' in df.columns and 'reorder_level' in df.columns:
                    df[col_name] = df['stock_level'] < df['reorder_level']
                    
                # Standardize type of enriched columns
                col_type = enrich.get('type')
                if col_type == 'integer':
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce').fillna(0).astype(int)
                elif col_type == 'float':
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce').fillna(0.0).astype(float)
                elif col_type == 'boolean':
                    df[col_name] = df[col_name].astype(bool)
            
            cleaned_rows = len(df)
            dropped_rows = raw_rows - cleaned_rows
            
            # 6. Save to CSV (Silver Layer)
            df.to_csv(dest_path, index=False)
            logger.info(f"Silver Process Success: '{dataset_name}' -> Saved to '{dest_path}' ({cleaned_rows} rows, dropped {dropped_rows} rows)")
            
            # 7. Save to SQL Database (SQLite)
            save_to_sql(df, f"silver_{dataset_name}", db_conn)
            logger.info(f"Silver table 'silver_{dataset_name}' successfully updated in SQLite database.")
            
            silver_metrics[dataset_name] = {
                "raw_rows": raw_rows,
                "cleaned_rows": cleaned_rows,
                "dropped_rows": dropped_rows,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to process silver layer for dataset '{dataset_name}': {str(e)}")
            db_conn.close()
            raise e
            
    db_conn.close()
    
    # Save silver metrics to a JSON file
    metrics_path = os.path.join(target_dir, "silver_metadata.json")
    with open(metrics_path, 'w') as f:
        json.dump(silver_metrics, f, indent=4)
        
    logger.info(f"Silver layer processing complete. Metadata saved to {metrics_path}")
    return silver_metrics
if __name__ == "__main__":
    run_silver_layer()