import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import json
import shutil
import pandas as pd
from datetime import datetime
from utils import load_config, setup_logger

print(">>> Bronze script started")

def run_bronze_layer():
    print(">>> Entered run_bronze_layer()")

    try:
        config = load_config()
        print(">>> Configuration loaded successfully")

        logger = setup_logger()
        print(">>> Logger initialized")

        logger.info("Starting Bronze Layer Ingestion...")

        bronze_config = config["layers"]["bronze"]
        source_dir = bronze_config["source_dir"]
        target_dir = bronze_config["target_dir"]

        print(f">>> Source Directory: {source_dir}")
        print(f">>> Target Directory: {target_dir}")

        # Adjust paths if running from scripts directory
        if not os.path.exists(source_dir):
            source_dir = os.path.join("..", source_dir)
            target_dir = os.path.join("..", target_dir)

        print(f">>> Using Source: {os.path.abspath(source_dir)}")
        print(f">>> Using Target: {os.path.abspath(target_dir)}")

        os.makedirs(target_dir, exist_ok=True)

        ingestion_metrics = []

        for dataset in bronze_config["datasets"]:
            name = dataset["name"]
            filename = dataset["file"]

            src_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(target_dir, f"{name}.csv")

            print(f"\n>>> Processing {name}")
            print(f"Source : {src_path}")
            print(f"Target : {dest_path}")

            if not os.path.exists(src_path):
                print(f"File not found: {src_path}")
                continue

            df = pd.read_csv(src_path)

            rows, cols = df.shape
            file_size_kb = os.path.getsize(src_path) / 1024

            shutil.copy2(src_path, dest_path)

            logger.info(
                f"Copied {name} ({rows} rows, {cols} columns)"
            )

            ingestion_metrics.append({
                "dataset": name,
                "source_file": src_path,
                "target_file": dest_path,
                "rows": rows,
                "columns": cols,
                "file_size_kb": round(file_size_kb, 2),
                "timestamp": datetime.now().isoformat()
            })

        metadata_path = os.path.join(target_dir, "ingestion_metadata.json")

        with open(metadata_path, "w") as f:
            json.dump(ingestion_metrics, f, indent=4)

        print("\nBronze Layer Completed Successfully!")
        print(f"Metadata saved to {metadata_path}")

    except Exception as e:
        print("\n ERROR OCCURRED")
        print(type(e).__name__)
        print(e)
        raise


if __name__ == "__main__":
    print(">>> Main block executing")
    run_bronze_layer()