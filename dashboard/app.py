import os
import sys
import json
import sqlite3
import pandas as pd
import streamlit as st
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Set up page configurations
st.set_page_config(
    page_title="RetailPulse Supply Chain Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom Styling (Dark Mode Accents)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f3f4f6;
        padding: 1.2rem;
        border-radius: 0.5rem;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
    }
</style>
""", unsafe_allow_html=True)
# Utility Functions
def load_config():
    config_path = os.path.join(BASE_DIR, "pipeline_config.yaml")

    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    return {}


def run_pipeline_command(engine):
    import subprocess

    config = load_config()

    config_path = os.path.join(BASE_DIR, "pipeline_config.yaml")

    if config:
        config["pipeline"]["engine"] = engine

        with open(config_path, "w") as file:
            yaml.dump(config, file)

    pipeline_path = os.path.join(BASE_DIR, "run_pipeline.py")

    result = subprocess.run(
        [sys.executable, pipeline_path],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    return result.returncode == 0, result.stdout, result.stderr



def get_db_data(query):

    db_path = os.path.join(BASE_DIR, "data", "retailpulse.db")

    if not os.path.exists(db_path):
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame({"Error":[str(e)]})
        
# Load configurations
config = load_config()
# Sidebar Setup
st.sidebar.title("RetailPulse Controls")
st.sidebar.markdown("Manage and run the Medallion data engineering pipeline.")
engine_choice = st.sidebar.selectbox(
    "Execution Engine",
    options=["Pandas", "Spark"],
    index=0 if config.get('pipeline', {}).get('engine', 'pandas') == 'pandas' else 1
)
if st.sidebar.button(" Run Pipeline Ingest & Process", use_container_width=True):
    with st.spinner(f"Running pipeline with {engine_choice} engine..."):
        success, stdout, stderr = run_pipeline_command(engine_choice.lower())
        if success:
            st.sidebar.success("Pipeline executed successfully!")
            st.toast("Pipeline completed!")
        else:
            st.sidebar.error("Pipeline run failed. Check logs.")
            st.toast("Pipeline failed!")
        # Show log modal/expander
        with st.sidebar.expander("Show Console Output"):
            st.code(stdout)
            if stderr:
                st.code(stderr)
st.sidebar.divider()
st.sidebar.markdown("""
**Medallion Layers:**
-  **Bronze Layer**: Raw CSV copy
-  **Silver Layer**: Cleaned & Enriched
-  **Gold Layer**: Aggregated KPIs
""")
# Main Content
st.markdown('<p class="main-header">RetailPulse Supply Chain Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">End-to-End Retail Supply Chain Pipeline using Medallion Architecture</p>', unsafe_allow_html=True)
# Fetch Metrics
total_revenue = 0
total_orders = 0
active_alerts = 0
top_store_name = "N/A"
revenue_df = get_db_data("SELECT SUM(total_value) as rev, COUNT(order_id) as ords FROM silver_orders")
if not revenue_df.empty and pd.notna(revenue_df.iloc[0]['rev']):
    total_revenue = revenue_df.iloc[0]['rev']
    total_orders = revenue_df.iloc[0]['ords']
alerts_df = get_db_data("SELECT COUNT(*) as cnt FROM gold_low_stock_alerts")
if not alerts_df.empty:
    active_alerts = alerts_df.iloc[0]['cnt']
top_store_df = get_db_data("SELECT store_name FROM gold_store_performance LIMIT 1")
if not top_store_df.empty:
    top_store_name = top_store_df.iloc[0]['store_name']
# Metrics display
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Total Revenue</div>
        <div class="metric-value">₹{total_revenue:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10b981;">
        <div class="metric-title"> Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #ef4444;">
        <div class="metric-title"> Stockout Alerts</div>
        <div class="metric-value">{active_alerts}</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #f59e0b;">
        <div class="metric-title"> Top Performing Store</div>
        <div class="metric-value" style="font-size: 1.25rem; padding-top: 0.5rem;">{top_store_name}</div>
    </div>
    """, unsafe_allow_html=True)
st.write("")
# Tabs setup
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " Pipeline Overview", 
    " Medallion Data Viewer", 
    " KPIs & Analytics", 
    " SQL Workbench",
    " Pipeline Config & Run Logs"
])
with tab1:
    st.subheader("Medallion Architecture Flow")
    st.write("This pipeline moves data through three structured stages to refine and validate raw retail records.")
    
    # Diagram/Architecture explanation
    flow_col1, flow_col2, flow_col3 = st.columns(3)
    with flow_col1:
        st.info("###  Bronze (Raw)\nIngests raw CSV data exactly as-is into `data/bronze/` to preserve historical lineage.")
        ingest_meta_path = "data/bronze/ingestion_metadata.json"
        if os.path.exists(ingest_meta_path):
            with open(ingest_meta_path, "r") as f:
                meta = json.load(f)
            st.json(meta)
            
    with flow_col2:
        st.success("###  Silver (Cleaned)\nCleans null values, removes duplicates, validates schemas, and enriches fields (e.g. `total_value` & `low_stock_flag`).")
        silver_meta_path = "data/silver/silver_metadata.json"
        if os.path.exists(silver_meta_path):
            with open(silver_meta_path, "r") as f:
                meta = json.load(f)
            st.json(meta)
            
    with flow_col3:
        st.warning("###  Gold (Insights)\nComputes business KPIs, joins reference dimensions, and runs SQL aggregates for analytics.")
        gold_meta_path = "data/gold/gold_metadata.json"
        if os.path.exists(gold_meta_path):
            with open(gold_meta_path, "r") as f:
                meta = json.load(f)
            st.json(meta)
with tab2:
    st.subheader("Explore Medallion Datasets")
    st.write("Select a layer and a dataset to view previews.")
    
    view_layer = st.radio("Select Medallion Layer", ["Bronze (Raw)", "Silver (Cleaned)"], horizontal=True)
    
    dataset_to_view = st.selectbox(
        "Select Dataset",
        ["orders", "inventory", "products", "stores", "suppliers"]
    )
    
    if view_layer == "Bronze (Raw)":
        csv_path = f"data/bronze/{dataset_to_view}.csv"
    else:
        csv_path = f"data/silver/{dataset_to_view}_clean.csv"
        
    if os.path.exists(csv_path):
        df_preview = pd.read_csv(csv_path)
        st.markdown(f"**Showing preview for: `{csv_path}` ({len(df_preview)} total rows)**")
        st.dataframe(df_preview.head(100), use_container_width=True)
        st.write(f"Schema Details:")
        st.dataframe(pd.DataFrame(df_preview.dtypes.astype(str), columns=["Data Type"]))
    else:
        st.warning(f"File not found: `{csv_path}`. Make sure to run the pipeline first!")
with tab3:
    st.subheader("Gold Layer Key Performance Indicators (KPIs)")
    
    kpi_tab1, kpi_tab2, kpi_tab3 = st.tabs([" Sales & Product performance", " Low Stock Alerts", " Saved Visualizations"])
    
    with kpi_tab1:
        st.write("#### Top Products by Revenue")
        top_prod_df = get_db_data("SELECT * FROM gold_top_products")
        if not top_prod_df.empty:
            st.dataframe(top_prod_df, use_container_width=True)
        else:
            st.warning("No data found in `gold_top_products` table.")
            
        st.write("#### Store Performance")
        store_perf_df = get_db_data("SELECT * FROM gold_store_performance")
        if not store_perf_df.empty:
            st.dataframe(store_perf_df, use_container_width=True)
        else:
            st.warning("No data found in `gold_store_performance` table.")
            
        st.write("#### Category Revenue Performance")
        cat_rev_df = get_db_data("SELECT * FROM gold_category_revenue")
        if not cat_rev_df.empty:
            st.dataframe(cat_rev_df, use_container_width=True)
        else:
            st.warning("No data found in `gold_category_revenue` table.")
            
    with kpi_tab2:
        st.write("#### Low Stock Alerts (Stockout Risks)")
        st.markdown("Products whose current stock level is below the reorder threshold, requiring immediate attention.")
        low_stock_df = get_db_data("SELECT * FROM gold_low_stock_alerts")
        if not low_stock_df.empty:
            st.dataframe(low_stock_df.style.background_gradient(subset=['units_needed'], cmap='Reds'), use_container_width=True)
        else:
            st.success("No stockout risks identified! All products are well stocked.")
            
    with kpi_tab3:
        st.write("#### Saved Static Pipeline Reports & Charts")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            if os.path.exists("outputs/top_10_products_revenue.png"):
                st.image("outputs/top_10_products_revenue.png", caption="Top 10 Products by Revenue", use_container_width=True)
            else:
                st.info("Chart 'top_10_products_revenue.png' not generated yet.")
                
            if os.path.exists("outputs/store_revenue_performance.png"):
                st.image("outputs/store_revenue_performance.png", caption="Store Performance comparison", use_container_width=True)
            else:
                st.info("Chart 'store_revenue_performance.png' not generated yet.")
                
        with chart_col2:
            if os.path.exists("outputs/daily_revenue_trend.png"):
                st.image("outputs/daily_revenue_trend.png", caption="Daily Revenue Trend", use_container_width=True)
            else:
                st.info("Chart 'daily_revenue_trend.png' not generated yet.")
with tab4:
    st.subheader("Interactive SQL Workbench")
    st.write("Run raw SQL queries against the local SQLite warehouse database `data/retailpulse.db`.")
    
    st.markdown("""
    **Available tables:**
    - `silver_orders`, `silver_inventory`, `silver_products`, `silver_stores`, `silver_suppliers`
    - `gold_low_stock_alerts`, `gold_daily_sales`, `gold_top_products`, `gold_store_performance`, `gold_category_revenue`
    """)
    
    default_query = "SELECT * FROM gold_store_performance WHERE region = 'South' LIMIT 5"
    sql_query = st.text_area("Write SQL Query", value=default_query, height=100)
    
    if st.button(" Run SQL Query"):
        with st.spinner("Executing query..."):
            query_res = get_db_data(sql_query)
            st.write(f"Returned {len(query_res)} rows:")
            st.dataframe(query_res, use_container_width=True)
with tab5:
    st.subheader("Pipeline Log files & Config File")
    
    log_tabs = st.tabs(["Pipeline Logs (`logs/pipeline.log`)", "Configuration File (`pipeline_config.yaml`)", "Pipeline Run Report"])
    
    with log_tabs[0]:
        log_path = "logs/pipeline.log"
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            st.text_area("Last 150 Lines of Logs", value="".join(lines[-150:]), height=400)
        else:
            st.info("Log file not generated yet. Run the pipeline first.")
            
    with log_tabs[1]:
        if os.path.exists("pipeline_config.yaml"):
            with open("pipeline_config.yaml", "r") as f:
                config_content = f.read()
            st.code(config_content, language="yaml")
        else:
            st.warning("pipeline_config.yaml not found.")
            
    with log_tabs[2]:
        report_path = "data/pipeline_run_report.json"
        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                report = json.load(f)
            st.json(report)
        else:
            st.info("Pipeline run report not generated yet. Run the pipeline.")