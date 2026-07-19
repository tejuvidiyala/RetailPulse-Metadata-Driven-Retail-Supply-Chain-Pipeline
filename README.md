# RetailPulse — Retail Supply Chain Data Pipeline

## Structure
- data/raw     -> original CSVs, untouched
- data/bronze  -> ingested, unmodified copies
- data/silver  -> cleaned, validated, typed data
- data/gold    -> KPI tables for dashboard/analytics
- scripts/     -> bronze_ingest.py, silver_clean.py, gold_kpis.py
- sql/         -> equivalent SQL for every KPI
- dashboard/   -> Streamlit app (reads Gold layer only)
- notebooks/   -> exploration only, never required for pipeline to run
- logs/        -> pipeline run logs


#  RetailPulse – Smart Metadata-Driven Retail Supply Chain Analytics Pipeline

---

#  Project Overview

RetailPulse is an end-to-end Retail Supply Chain Analytics Pipeline developed using the **Medallion Architecture (Bronze → Silver → Gold)**. The project demonstrates how raw retail operational data can be transformed into clean, reliable, and analytics-ready information using a metadata-driven approach.

The pipeline processes multiple retail datasets, including Orders, Inventory, Products, Stores, and Suppliers, through three structured data layers. Each layer progressively improves data quality by performing ingestion, validation, cleansing, enrichment, aggregation, and business analytics generation.

The processed data is stored in a centralized SQLite warehouse and visualized through an interactive Streamlit dashboard that provides real-time business insights, SQL query capabilities, KPI monitoring, and automated visualization charts.

The entire workflow is driven by a YAML configuration file, making the pipeline metadata-driven, reusable, scalable, and easy to maintain without modifying application logic whenever business rules change.

---

# Problem Statement

Retail organizations generate massive volumes of operational data every day from sales transactions, inventory systems, supplier records, product catalogs, and store operations. Although this information is extremely valuable, it is often stored in separate files or systems without any standardized processing mechanism.

Raw operational datasets generally contain inconsistent formats, duplicate records, missing values, invalid data types, and disconnected business entities. Such poor-quality data makes reporting unreliable and significantly slows down business decision-making.

Without a centralized processing pipeline, organizations face several operational challenges, including delayed business reporting, inaccurate inventory tracking, stock shortages, excess inventory, inconsistent product information, and poor visibility into overall supply chain performance.

Business analysts and management teams therefore spend considerable time manually cleaning and preparing data before any meaningful analysis can be performed.

RetailPulse addresses these challenges by implementing a structured, metadata-driven data engineering pipeline that automatically transforms raw retail data into clean, validated, enriched, and business-ready datasets while preserving complete data lineage across the Medallion Architecture.

---

#  Project Objectives

The primary objective of RetailPulse is to design and implement a production-inspired Retail Supply Chain Analytics Pipeline using modern Data Engineering principles.

The project aims to achieve the following objectives:

- Develop a complete Medallion Architecture consisting of Bronze, Silver, and Gold layers.
- Automate the ingestion of multiple retail datasets.
- Improve overall data quality through validation and cleansing.
- Eliminate duplicate records and handle missing values.
- Perform schema validation using metadata-driven rules.
- Enrich datasets with derived business attributes.
- Generate analytical Key Performance Indicators (KPIs).
- Store processed datasets inside a centralized SQLite analytical warehouse.
- Provide SQL-based analytics through an integrated SQL Workbench.
- Build an interactive Streamlit dashboard for business visualization.
- Generate automated business charts for management reporting.
- Maintain complete execution logs and metadata for auditing purposes.
- Support both Pandas and PySpark execution engines through configuration.

---

#  Business Use Case

Retail businesses continuously monitor sales, inventory availability, supplier performance, product demand, and store operations to improve customer satisfaction and operational efficiency.

However, when data exists across multiple disconnected systems, obtaining reliable business insights becomes both time-consuming and error-prone.

RetailPulse simulates a real-world retail data engineering solution by integrating multiple operational datasets into a unified analytics pipeline.

The generated insights enable businesses to:

- Monitor total sales revenue.
- Track daily sales performance.
- Identify top-selling products.
- Measure store-level revenue.
- Analyze category-wise sales.
- Detect low inventory before stockouts occur.
- Support inventory replenishment planning.
- Improve supply chain visibility.
- Enable faster management reporting.
- Reduce manual reporting effort.

By converting operational data into business intelligence, RetailPulse demonstrates how modern data engineering pipelines directly contribute to better business decision-making.

---

#  Solution Overview

RetailPulse follows the Medallion Architecture, an industry-standard data engineering design pattern widely adopted in modern Lakehouse implementations.

Instead of processing raw datasets directly for analytics, the pipeline progressively refines data across multiple stages.

The processing flow follows:

Raw CSV Files
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
SQLite Warehouse
        ↓
Streamlit Dashboard

Each layer has a clearly defined responsibility.

The Bronze layer preserves original data exactly as received.

The Silver layer improves data quality through validation, standardization, duplicate removal, schema enforcement, and enrichment.

The Gold layer generates analytical datasets optimized for business reporting.

Finally, processed information is stored inside SQLite and presented through an interactive Streamlit dashboard.

---

#  Medallion Architecture

The project follows a three-layer Medallion Architecture.

##  Bronze Layer

The Bronze layer acts as the raw landing zone.

Its responsibility is to ingest source CSV files exactly as received without modifying any values.

No cleansing or transformations are performed during this stage.

The objective is to preserve historical lineage and maintain an immutable copy of the original datasets.

Metadata regarding file size, row count, column count, ingestion timestamp, and processing information is automatically generated.

---

##  Silver Layer

The Silver layer is responsible for improving data quality.

This stage validates schemas, converts data types, removes duplicate records, handles missing values, applies business validation rules, and creates enriched business attributes.

Examples include:

- Computing Total Order Value
- Creating Low Stock Flags
- Standardizing Date Formats
- Primary Key Validation

The cleaned datasets become trusted sources for analytical processing.

---

##  Gold Layer

The Gold layer transforms validated operational data into business intelligence.

Instead of storing transactional information, this layer generates analytical reports and KPIs.

Examples include:

- Daily Sales Report
- Top Selling Products
- Category Revenue
- Store Performance
- Low Stock Alerts

These datasets are optimized for dashboards, management reporting, and SQL analytics.

---

#  Key Features

RetailPulse includes several production-inspired features that demonstrate modern data engineering practices.

 Metadata-driven pipeline using YAML configuration.

 Medallion Architecture implementation.

 Automated ETL workflow.

 Schema validation.

 Duplicate detection and removal.

 Missing value handling.

 Business data enrichment.

 SQLite analytical warehouse.

 SQL Workbench integration.

 Interactive Streamlit dashboard.

 Automated chart generation.

 Centralized logging and execution monitoring.

 Configurable execution engine (Pandas / PySpark).

 Modular and reusable project structure.

 End-to-end business KPI generation.


#  Project Structure

RetailPulse follows a modular project structure where each component has a dedicated responsibility. This separation of concerns improves maintainability, scalability, readability, and reusability of the entire pipeline.

```
RetailPulse/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── retailpulse.db
│   └── pipeline_run_report.json
│
├── images/
│
├── logs/
│   └── pipeline.log
│
├── outputs/
│   ├── top_10_products_revenue.png
│   ├── daily_revenue_trend.png
│   └── store_revenue_performance.png
│
├── scripts/
│   ├── bronze_ingest.py
│   ├── silver_clean.py
│   ├── gold_kpis.py
│   ├── generate_charts.py
│   └── utils.py
│
├── pipeline_config.yaml
├── run_pipeline.py
├── requirements.txt
└── README.md
```

Each folder in the project has a specific purpose.

###  dashboard/

This folder contains the Streamlit application that serves as the user interface of RetailPulse.

The dashboard enables users to execute the pipeline, monitor KPIs, visualize business insights, run SQL queries, inspect metadata generated by each Medallion layer, and review pipeline execution logs.

---

###  data/

The `data` directory stores all datasets processed by the pipeline.

It is divided into four stages representing the Medallion Architecture.

**raw/**

Contains the original source CSV files received by the pipeline.

**bronze/**

Contains raw copies of all datasets after ingestion along with ingestion metadata.

**silver/**

Stores cleaned and validated datasets after schema enforcement, duplicate removal, null handling, and business enrichment.

**gold/**

Stores analytical datasets generated from business aggregations such as Daily Sales, Top Products, Store Performance, Category Revenue, and Low Stock Alerts.

The folder also contains:

- `retailpulse.db` – SQLite analytical warehouse.
- `pipeline_run_report.json` – Execution summary generated after each pipeline run.

---

###  scripts/

The `scripts` directory contains the core business logic of the pipeline.

Each Python script represents one independent stage of the data engineering workflow.

This modular architecture makes the project easier to maintain and extend.

---

###  outputs/

Contains visualization charts automatically generated after Gold Layer processing.

Charts include:

- Daily Revenue Trend
- Top 10 Products by Revenue
- Store Performance

These visualizations are displayed inside the Streamlit dashboard.

---

### logs/

Stores centralized execution logs.

Every pipeline activity including ingestion, cleansing, aggregation, chart generation, and execution time is recorded inside `pipeline.log`.

This enables debugging, monitoring, and auditing.

---

#  Dataset Description

RetailPulse uses five retail datasets that simulate a real-world retail supply chain environment.

---

## Orders Dataset

The Orders dataset contains transactional information about customer purchases.

Each record represents a single purchase made at a retail store.

Important attributes include:

- Order ID
- Order Date
- Product ID
- Quantity
- Price
- Store ID

This dataset is the primary source for revenue calculations and sales analytics.

During Silver Layer processing, a new business attribute called **Total Value** is generated using:

```
Total Value = Quantity × Price
```

---

## Inventory Dataset

The Inventory dataset stores stock availability information for every product across different retail stores.

Key attributes include:

- Product ID
- Store ID
- Stock Level
- Reorder Level
- Last Updated

During Silver Layer processing, RetailPulse generates a business flag:

```
Low Stock Flag
```

This flag identifies products that require replenishment before inventory reaches critical levels.

The logic used is:

```
Stock Level < Reorder Level
```

---

## Products Dataset

The Products dataset acts as the product master table.

It contains product-specific information including:

- Product ID
- Product Name
- Category
- Supplier ID

This dataset is primarily used for joining product details during Gold Layer analytics.

---

## Stores Dataset

The Stores dataset contains geographical and organizational information for each retail outlet.

Attributes include:

- Store ID
- Store Name
- City
- Region

This dataset enables store-wise revenue analysis and regional performance reporting.

---

## Suppliers Dataset

The Suppliers dataset contains supplier master information.

Important attributes include:

- Supplier ID
- Supplier Name
- Contact City
- Lead Time
- Supplier Rating

Although supplier analytics are not directly visualized in the dashboard, the dataset establishes relationships with products and can easily be extended for supplier performance reporting.

---

# 🛠 Technologies Used

RetailPulse combines multiple open-source technologies to build a complete data engineering pipeline.

| Technology | Purpose |
|------------|---------|
| Python | Core programming language used to develop the entire pipeline |
| Pandas | Data ingestion, cleansing, enrichment, and transformations |
| SQLite | Lightweight analytical database for storing Silver and Gold datasets |
| SQL | Business analytics and KPI generation |
| Streamlit | Interactive dashboard and SQL workbench |
| PyYAML | Reading metadata-driven pipeline configuration |
| Matplotlib | Business visualization charts |
| Seaborn | Professional chart styling |
| Logging | Centralized execution monitoring |
| PySpark | Optional distributed processing engine |

---

## Why Python?

Python was selected because of its rich ecosystem for Data Engineering.

It provides excellent libraries for ETL, data manipulation, visualization, SQL integration, and dashboard development while keeping implementation simple and modular.

---

## Why Pandas?

Pandas provides high-performance DataFrame operations that simplify data cleansing, aggregation, joins, filtering, and business calculations.

It is well suited for local analytical workloads and rapid pipeline development.

---

## Why SQLite?

SQLite was chosen as the analytical warehouse because it requires no server installation while still supporting relational SQL queries.

It provides a lightweight solution for storing processed Silver and Gold datasets that can easily be accessed from the dashboard.

---

## Why Streamlit?

Streamlit enables rapid development of interactive data applications using only Python.

It allows business users to explore KPIs, execute SQL queries, monitor pipeline execution, and visualize analytics without writing code.

---

## Why YAML?

Instead of hardcoding schemas, validation rules, and business logic inside Python scripts, RetailPulse stores pipeline metadata inside `pipeline_config.yaml`.

This makes the pipeline highly configurable and significantly improves maintainability.

Changing validation rules or adding new datasets requires only metadata updates rather than modifying application logic.

---

#  End-to-End Workflow

RetailPulse follows a structured workflow where data progressively moves through multiple processing stages.

```
Raw CSV Files
      │
      ▼
Bronze Layer
      │
      ▼
Silver Layer
      │
      ▼
Gold Layer
      │
      ▼
SQLite Warehouse
      │
      ▼
Charts + Dashboard
```

Each stage has a clearly defined responsibility, ensuring data quality, consistency, traceability, and business readiness before analytics are generated.

#  Pipeline Implementation

RetailPulse follows a modular ETL (Extract, Transform, Load) architecture where every stage of the pipeline is implemented as an independent Python module. This modular approach improves code readability, maintainability, testing, and scalability while ensuring that each component has a single responsibility.

The pipeline execution is orchestrated through `run_pipeline.py`, which sequentially triggers each processing layer and records execution details.

The complete execution flow is illustrated below.

```
Raw CSV Files
       │
       ▼
Bronze Layer (Ingestion)
       │
       ▼
Silver Layer (Cleaning & Validation)
       │
       ▼
Gold Layer (Business KPIs)
       │
       ▼
SQLite Warehouse
       │
       ▼
Charts Generation
       │
       ▼
Streamlit Dashboard
```

---

#  Bronze Layer

## Purpose

The Bronze layer is the first stage of the Medallion Architecture. Its primary objective is to ingest raw retail datasets exactly as they are received without performing any transformations.

This layer preserves the original data, ensuring complete data lineage and enabling recovery if downstream processing fails.

The Bronze layer serves as the foundation for all subsequent processing stages.

---

## Script

```
scripts/bronze_ingest.py
```

---

## Responsibilities

The Bronze layer performs the following operations:

- Reads all source CSV files from the `data/raw` directory.
- Copies each dataset into the Bronze directory.
- Preserves the original file contents without modification.
- Records dataset statistics.
- Generates ingestion metadata.
- Writes execution logs.

---

## Input

```
data/raw/
```

Contains:

- orders.csv
- inventory.csv
- products.csv
- stores.csv
- suppliers.csv

---

## Output

```
data/bronze/
```

Generated files include:

- orders.csv
- inventory.csv
- products.csv
- stores.csv
- suppliers.csv
- ingestion_metadata.json

---

## Metadata Generated

For every dataset the Bronze layer records:

- Dataset Name
- Source File
- Target File
- Number of Rows
- Number of Columns
- File Size
- Timestamp

Example

```
Orders

Rows : 600

Columns : 6

Timestamp :
2026-07-17T17:39:08
```

---

## Benefits

- Preserves raw data.
- Maintains audit history.
- Enables pipeline recovery.
- Supports data lineage.

---

#  Silver Layer

## Purpose

The Silver layer is responsible for improving data quality.

Instead of directly using raw operational data, RetailPulse validates, standardizes, and enriches the datasets before analytics are generated.

The Silver layer converts raw operational data into trusted business data.

---

## Script

```
scripts/silver_clean.py
```

---

## Responsibilities

The Silver layer performs:

- Schema validation
- Data type conversion
- Missing value removal
- Duplicate removal
- Primary key validation
- Business enrichment
- SQLite synchronization

---

## Cleaning Rules

The validation rules are not hardcoded.

Instead, they are dynamically loaded from

```
pipeline_config.yaml
```

This makes the pipeline metadata-driven.

Whenever validation rules change, only the YAML file needs to be updated.

---

## Orders Processing

The Orders dataset undergoes the following transformations.

### Schema Validation

Validates columns such as

- order_id
- order_date
- quantity
- price

against metadata.

---

### Null Handling

Rows containing missing values in important columns are removed.

---

### Duplicate Removal

Duplicate Order IDs are removed.

This ensures that each transaction appears only once.

---

### Data Enrichment

A new business column is created.

```
Total Value

=

Quantity × Price
```

Example

```
Quantity

5

Price

₹120

↓

Total Value

₹600
```

This column is later used for revenue analytics.

---

## Inventory Processing

Inventory data is validated similarly.

A business flag is generated.

```
Low Stock Flag

=

Stock Level

<

Reorder Level
```

Example

```
Stock Level

25

Reorder Level

50

↓

Low Stock

TRUE
```

This enrichment enables automatic stockout detection.

---

## Products Processing

Processing includes:

- Schema validation
- Duplicate removal
- Null checking

The cleaned product table later supports joins during KPI generation.

---

## Stores Processing

Validates

- Store ID
- Store Name
- City
- Region

This dataset enables store-level analytics.

---

## Suppliers Processing

Performs

- Duplicate removal
- Schema validation
- Null checking

Supplier information is preserved for future analytical extensions.

---

## SQLite Synchronization

After every cleaned dataset is generated, it is automatically stored inside SQLite.

Tables created include:

```
silver_orders

silver_inventory

silver_products

silver_stores

silver_suppliers
```

---

## Output

```
data/silver/
```

Contains

- orders_clean.csv
- inventory_clean.csv
- products_clean.csv
- stores_clean.csv
- suppliers_clean.csv
- silver_metadata.json

---

#  Gold Layer

## Purpose

The Gold layer converts cleaned operational data into business intelligence.

Instead of transaction-level information, this layer produces analytical datasets that answer business questions.

These outputs are optimized for dashboards and reporting.

---

## Script

```
scripts/gold_kpis.py
```

---

## Responsibilities

The Gold layer performs:

- Dataset joins
- Business aggregations
- Revenue calculations
- KPI generation
- SQLite synchronization
- Metadata generation

---

# KPI 1 — Daily Sales

Purpose

Provides daily business performance.

Calculations

- Total Orders
- Total Revenue
- Average Order Value

Grouped By

```
Order Date
```

Output

```
daily_sales.csv
```

Business Value

Management can monitor sales trends over time.

---

# KPI 2 — Top Products

Purpose

Identifies products generating the highest revenue.

Calculations

```
SUM(Total Value)

SUM(Quantity)
```

Grouped By

```
Product Name

Category
```

Returns

Top 10 Products

Output

```
top_products.csv
```

Business Value

Supports demand planning and marketing decisions.

---

# KPI 3 — Store Performance

Purpose

Measures store-wise revenue.

Calculations

- Total Orders
- Total Revenue

Grouped By

- Store
- City
- Region

Output

```
store_performance.csv
```

Business Value

Identifies high-performing and low-performing retail outlets.

---

# KPI 4 — Category Revenue

Purpose

Measures category-wise business performance.

Calculations

```
Revenue

Units Sold
```

Grouped By

```
Category
```

Output

```
category_revenue.csv
```

Business Value

Helps understand which product categories contribute the highest revenue.

---

# KPI 5 — Low Stock Alerts

Purpose

Detects products requiring replenishment.

Logic

```
Stock Level

<

Reorder Level
```

Additional Calculation

```
Units Needed

=

Reorder Level

-

Stock Level
```

Example

```
Stock

20

Reorder

50

↓

Units Needed

30
```

Output

```
low_stock_alerts.csv
```

Business Value

Helps inventory managers avoid stockouts and maintain product availability.

---

## SQLite Storage

All Gold datasets are automatically synchronized into SQLite.

Tables include

- gold_daily_sales
- gold_top_products
- gold_store_performance
- gold_category_revenue
- gold_low_stock_alerts

These tables are later queried directly from the Streamlit dashboard.

---

#  Chart Generation

## Script

```
scripts/generate_charts.py
```

After the Gold Layer completes successfully, the pipeline automatically generates business visualizations.

Charts generated include:

- Daily Revenue Trend
- Top 10 Products by Revenue
- Store Revenue Performance

The charts are saved inside the `outputs/` directory and displayed in the dashboard.

These visualizations help business users quickly identify sales trends, product performance, and store-wise revenue distribution without writing SQL queries.


#  Utility Module

## Script

```
scripts/utils.py
```

The `utils.py` module contains reusable utility functions that are shared across the entire RetailPulse pipeline. Instead of rewriting common functionality in every script, all helper methods are centralized inside this module, improving code reusability and maintainability.

The utilities include:

- Loading the YAML configuration file.
- Creating a centralized logging system.
- Establishing SQLite database connections.
- Saving DataFrames into SQLite tables.
- Executing SQL queries.
- Initializing an optional PySpark session.

This modular design reduces code duplication and follows software engineering best practices.

---

#  Pipeline Configuration

## File

```
pipeline_config.yaml
```

RetailPulse is designed as a metadata-driven pipeline.

Instead of hardcoding business rules inside Python scripts, all configuration parameters are stored in the YAML file.

The configuration file controls:

- Dataset locations
- Source directories
- Target directories
- Schema definitions
- Data types
- Primary keys
- Duplicate removal rules
- Null validation rules
- Business enrichments
- KPI aggregations
- Join conditions
- Sorting rules
- Output file names
- Database configuration
- Execution engine

This design makes the pipeline highly configurable. Any business rule can be modified simply by updating the YAML configuration without changing the application code.

---

#  Pipeline Orchestration

## Script

```
run_pipeline.py
```

The `run_pipeline.py` script acts as the central controller of the entire RetailPulse project.

It sequentially executes every processing stage while monitoring execution time, logging progress, and generating execution reports.

The execution flow is:

```
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
Chart Generation
        ↓
Execution Report
```

During execution, the pipeline performs the following tasks:

- Initializes logging.
- Loads metadata configuration.
- Executes Bronze ingestion.
- Executes Silver cleansing.
- Executes Gold KPI generation.
- Generates business charts.
- Creates execution summary.
- Stores execution report.
- Updates pipeline logs.

If any stage fails, the pipeline records the error while preserving logs for debugging.

---

#  Streamlit Dashboard

## File

```
dashboard/app.py
```

RetailPulse includes an interactive Streamlit dashboard that provides a graphical interface for monitoring the complete data engineering pipeline.

Instead of manually executing SQL queries or opening CSV files, business users can explore the processed data through an intuitive web interface.

The dashboard acts as a centralized monitoring portal for both technical users and business stakeholders.

---

# Dashboard Features

## Pipeline Controls

Users can execute the complete pipeline directly from the dashboard.

The dashboard provides:

- Engine Selection
- Pipeline Execution Button
- Console Output
- Execution Status

This allows users to rerun the ETL workflow without using the terminal.

---

## KPI Cards

The dashboard displays key business metrics at the top.

Examples include:

- Total Revenue
- Total Orders
- Stockout Alerts
- Top Performing Store

These KPIs provide an instant overview of business performance.

---

## Medallion Layer Viewer

The dashboard displays metadata generated from every processing layer.

### Bronze Layer

Displays:

- Dataset Name
- Row Count
- Column Count
- File Size
- Timestamp

### Silver Layer

Displays:

- Raw Rows
- Cleaned Rows
- Dropped Rows
- Processing Timestamp

### Gold Layer

Displays:

- Generated KPIs
- Number of Rows
- Output Columns
- Generation Timestamp

This provides complete transparency into the ETL process.

---

#  Business Analytics

The dashboard provides interactive analytics generated from Gold Layer outputs.

Business users can explore:

- Revenue trends
- Product performance
- Store performance
- Category revenue
- Inventory alerts

These reports enable faster business decision-making.

---

#  Visualization Charts

RetailPulse automatically generates business visualizations after pipeline execution.

The following charts are available:

## Daily Revenue Trend

Displays revenue variation across different dates.

Business Insight:

Helps management identify seasonal demand patterns and revenue fluctuations.

---

## Top Products by Revenue

Displays the highest revenue-generating products.

Business Insight:

Supports marketing strategy, inventory planning, and product demand forecasting.

---

## Store Performance

Displays total revenue generated by each retail store.

Business Insight:

Helps compare store performance and identify high-performing locations.

---

#  SQL Workbench

RetailPulse includes an integrated SQL Workbench.

Users can execute custom SQL queries directly on the SQLite warehouse.

Example:

```sql
SELECT *
FROM gold_store_performance
ORDER BY total_revenue DESC;
```

The query results are displayed instantly within the dashboard.

This feature enables ad hoc business analysis without external SQL tools.

---

#  SQLite Data Warehouse

RetailPulse stores all processed datasets inside a centralized SQLite database.

The warehouse contains both Silver and Gold tables.

Examples include:

Silver Tables

- silver_orders
- silver_inventory
- silver_products
- silver_stores
- silver_suppliers

Gold Tables

- gold_daily_sales
- gold_top_products
- gold_store_performance
- gold_category_revenue
- gold_low_stock_alerts

SQLite enables efficient querying, dashboard integration, and centralized storage.

---

#  Logging

Every pipeline execution is recorded using Python's logging module.

Logs are written to:

```
logs/pipeline.log
```

The logging system captures:

- Pipeline start time
- Dataset processing
- Row counts
- KPI generation
- Chart generation
- SQL updates
- Errors
- Execution completion

Logging simplifies debugging and provides a complete audit trail.

---

#  Pipeline Execution Report

After every successful pipeline execution, a JSON report is automatically generated.

Location:

```
data/pipeline_run_report.json
```

The report contains:

- Pipeline Name
- Execution Timestamp
- Pipeline Status
- Total Execution Time
- Stage-wise Execution Summary

This report can be used for monitoring, auditing, and operational reporting.

---

#  Metadata-Driven Design

One of the major strengths of RetailPulse is its metadata-driven architecture.

Instead of embedding validation rules directly inside Python scripts, all business logic is configured externally through YAML metadata.

This approach provides several advantages:

- Easy maintenance
- Reduced code modifications
- Better scalability
- Faster onboarding of new datasets
- Reusable pipeline components

The pipeline dynamically reads configuration values and applies them during execution, making the solution flexible and production-oriented.

#  Project Results

The RetailPulse pipeline was successfully implemented and executed end-to-end using the Medallion Architecture. All pipeline stages completed successfully, and the processed datasets were transformed into business-ready analytical reports.

### Pipeline Execution Summary

| Stage | Status |
|--------|--------|
| Bronze Layer |  Completed |
| Silver Layer |  Completed |
| Gold Layer |  Completed |
| SQLite Integration |  Completed |
| Chart Generation |  Completed |
| Streamlit Dashboard |  Completed |

### Data Processing Statistics

| Dataset | Records Processed |
|----------|------------------:|
| Orders | 600 |
| Inventory | 300 |
| Products | 30 |
| Stores | 10 |
| Suppliers | 20 |

### Gold Layer Outputs

The pipeline successfully generated the following analytical datasets:

- Daily Sales Report
- Top Products Report
- Store Performance Report
- Category Revenue Report
- Low Stock Alerts Report

### Dashboard KPIs

The Streamlit dashboard displays real-time business metrics including:

- Total Revenue
- Total Orders
- Total Stockout Alerts
- Top Performing Store
- Business Charts
- SQL Query Results
- Pipeline Metadata
- Execution Logs

---

#  Business Insights Generated

RetailPulse transforms raw operational data into meaningful business insights that support decision-making.

### Revenue Analysis

The Daily Sales report provides day-wise revenue trends, enabling management to monitor business performance and identify periods of high or low sales activity.

### Product Performance

The Top Products report ranks products based on total revenue and units sold. This helps identify high-demand products for inventory planning and marketing campaigns.

### Store Performance

Store-wise analytics compare the revenue generated by each retail outlet. This helps management evaluate regional performance and identify top-performing stores.

### Category Revenue

Revenue is aggregated at the product category level, enabling businesses to understand which product categories contribute the most to overall sales.

### Inventory Monitoring

The Low Stock Alerts report identifies products where stock levels fall below the reorder threshold. The pipeline also calculates the number of units required to replenish inventory, helping reduce stockout risks.

---

#  Key Achievements

The project successfully demonstrates the following Data Engineering concepts:

- End-to-End ETL Pipeline Development
- Medallion Architecture Implementation
- Metadata-Driven Processing
- Automated Data Validation
- Data Cleansing and Enrichment
- Business KPI Generation
- SQLite Data Warehousing
- SQL Analytics
- Automated Chart Generation
- Interactive Streamlit Dashboard
- Logging and Execution Monitoring
- Modular Python Project Design

---

#  Challenges Faced

During the development of RetailPulse, several practical challenges were encountered and resolved.

### File Path Management

Initially, Python scripts and the Streamlit dashboard faced issues locating datasets because they were executed from different directories. This was resolved by implementing dynamic path handling using the `os` module.

---

### Metadata Configuration

Managing multiple validation rules, enrichment logic, and aggregation configurations directly inside Python scripts became difficult. This was solved by moving all configurable business rules into `pipeline_config.yaml`, making the pipeline metadata-driven.

---

### Dashboard Integration

Synchronizing the Streamlit dashboard with the latest pipeline outputs required ensuring that CSV files, SQLite tables, metadata files, and charts were refreshed after each successful execution.

---

### SQLite Synchronization

Automatically updating Silver and Gold datasets in SQLite required careful handling of table replacement and connection management to maintain consistency between CSV outputs and the analytical database.

---

### Chart Automation

Generating charts only after successful KPI generation required integrating chart creation into the pipeline workflow, ensuring visualizations always represented the latest processed data.

---

#  Advantages

RetailPulse provides several practical advantages:

- Modular project architecture.
- Metadata-driven processing reduces hardcoding.
- Reusable ETL components.
- Easy to maintain and extend.
- Centralized logging for monitoring.
- Automated report generation.
- Interactive dashboard for business users.
- SQLite integration for SQL analytics.
- Clear separation of Bronze, Silver, and Gold layers.
- Supports configurable execution through YAML.

---

#  Limitations

Although the project demonstrates a complete ETL workflow, it has certain limitations.

- The pipeline processes static CSV files rather than real-time streaming data.
- SQLite is suitable for local analytics but not for large-scale enterprise workloads.
- The dashboard is designed for a single local user and does not include authentication.
- PySpark support is optional and requires a Java environment.
- The project does not include automated scheduling or orchestration tools such as Apache Airflow.
- Data quality rules are limited to the implemented business validations.

These limitations provide opportunities for future enhancement.

---

#  Future Enhancements

RetailPulse can be extended with several enterprise-grade features.

### Real-Time Data Processing

Integrate Apache Kafka to ingest streaming retail transactions in real time.

---

### Workflow Orchestration

Use Apache Airflow to schedule and monitor ETL jobs automatically.

---

### Cloud Deployment

Deploy the pipeline on Azure or AWS using cloud storage and managed databases.

---

### Data Lakehouse

Replace SQLite with enterprise data platforms such as Delta Lake, Snowflake, or Azure Synapse for improved scalability.

---

### Machine Learning

Integrate demand forecasting models to predict future sales and inventory requirements.

---

### Advanced Analytics

Develop interactive dashboards using Power BI or Tableau alongside Streamlit.

---

### Authentication

Add role-based authentication to secure dashboard access.

---

### CI/CD Integration

Implement GitHub Actions to automate testing and deployment.

---

# Learning Outcomes

Through this project, the following concepts were learned and implemented:

- ETL Pipeline Development
- Medallion Architecture
- Data Validation Techniques
- Data Cleansing
- Metadata-Driven Design
- YAML Configuration
- SQL Database Integration
- SQLite Operations
- Business KPI Generation
- Data Visualization
- Streamlit Dashboard Development
- Logging and Monitoring
- Modular Python Programming
- End-to-End Data Engineering Workflow

---

#  Conclusion

RetailPulse successfully demonstrates the design and implementation of an end-to-end Retail Supply Chain Data Engineering Pipeline using the Medallion Architecture. The project transforms raw operational datasets into trusted analytical information through structured ingestion, validation, enrichment, and KPI generation.

The metadata-driven design makes the pipeline flexible, maintainable, and easy to extend, while the SQLite warehouse and Streamlit dashboard provide an accessible platform for business reporting and data exploration.

Overall, RetailPulse showcases practical Data Engineering skills including ETL development, data quality management, metadata-driven processing, SQL integration, dashboard development, and business analytics, making it a strong demonstration of production-inspired data engineering practices.

---


### Technologies

- Python
- Pandas
- SQLite
- SQL
- Streamlit
- Matplotlib
- Seaborn
- YAML
- PySpark (Optional)

---
