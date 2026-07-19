import os
import yaml
import logging
import sqlite3
import pandas as pd

#The load_config() function loads the pipeline_config.yaml file into a Python dictionary.
#It first checks whether the file exists in the current directory. 
#If not, it looks in the parent directory, allowing the script to
#work whether it is executed from the project root or the scripts folder.
#If the file is not found, it raises a FileNotFoundError. 
#Finally, it uses yaml.safe_load() to parse the YAML file
#into a dictionary that can be accessed throughout the pipeline.
def load_config(config_path="pipeline_config.yaml"):
    """Loads the YAML pipeline configuration file."""
    if not os.path.exists(config_path):
        # Check parent folder if running from scripts directory
        parent_path = os.path.join("..", config_path)
        if os.path.exists(parent_path):
            config_path = parent_path
        else:
            raise FileNotFoundError(f"Configuration file {config_path} not found.")           
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def setup_logger(log_dir="logs", log_file="pipeline.log"):
    """Sets up a logger that outputs to both console and file."""
    # Ensure logs directory exists
    # Adjust path if running from inside scripts
    if not os.path.exists(log_dir):
        if os.path.exists(os.path.join("..", log_dir)):
            log_dir = os.path.join("..", log_dir)
        else:
            os.makedirs(log_dir, exist_ok=True)
            
    log_path = os.path.join(log_dir, log_file)
    
    logger = logging.getLogger("RetailPulseLogger")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        
        # File Handler
        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        
        # Console Handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger


# Creates and returns a connection to the SQLite database.
# By default, the database file is stored in data/retailpulse.db.
def get_db_connection(db_path="data/retailpulse.db"):
    """Returns a SQLite database connection."""
# Check whether the 'data' folder exists.
# If the script is executed from the scripts folder,
# look for the data folder in the parent directory.
    if not os.path.exists("data") and os.path.exists("../data"):
        db_path = os.path.join("..", db_path)
    else:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
# Create the data directory if it doesn't already exist.
# exist_ok=True avoids an error if the folder is already present.
        
# Return the database connection object
# so other scripts can perform SQL operations.
    conn = sqlite3.connect(db_path)
    return conn




def save_to_sql(df, table_name, conn, if_exists="replace"):
    """Saves a Pandas DataFrame to a SQLite table."""
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def run_sql_query(query, conn):
    """Executes a SQL query and returns a Pandas DataFrame."""
    return pd.read_sql_query(query, conn)

# Initializes a PySpark session for distributed data processing.
# Imports SparkSession, sets the application name, configures the
# Spark warehouse directory and driver address, and creates or
# retrieves a Spark session. If PySpark or Java is not installed
# or configured correctly, it catches the exception and returns
# None, allowing the pipeline to fall back to the Pandas engine.
def init_spark_session(app_name="RetailPulsePipeline"):
    """Initializes and returns a PySpark session if available, else returns None."""
    try:
        from pyspark.sql import SparkSession
        # Build local Spark session
        spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.warehouse.dir", "spark-warehouse") \
            .config("spark.driver.bindAddress", "127.0.0.1") \
            .get_name() if hasattr(SparkSession.builder, 'get_name') else \
            SparkSession.builder.appName(app_name).getOrCreate()
        return spark
    except Exception as e:
        # PySpark not installed or Java not configured properly
        return None