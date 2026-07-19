import os
import sys
import time
import json
from datetime import datetime

# Add scripts folder to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.append(SCRIPTS_DIR)

from utils import setup_logger
from bronze_ingest import run_bronze_layer
from silver_clean import run_silver_layer
from gold_kpis import run_gold_layer
from generate_charts import generate_visualizations


def main():

    logger = setup_logger()

    logger.info("=" * 60)
    logger.info("Initializing RetailPulse Supply Chain Pipeline")
    logger.info("=" * 60)

    start_time = time.time()

    pipeline_status = "SUCCESS"

    execution_report = {}

    try:

        # ==========================
        # Bronze Layer
        # ==========================

        logger.info("[1/4] Running Bronze Layer...")

        t = time.time()

        run_bronze_layer()

        execution_report["Bronze"] = {
            "status": "SUCCESS",
            "duration_seconds": round(time.time() - t, 2)
        }

        # ==========================
        # Silver Layer
        # ==========================

        logger.info("[2/4] Running Silver Layer...")

        t = time.time()

        run_silver_layer()

        execution_report["Silver"] = {
            "status": "SUCCESS",
            "duration_seconds": round(time.time() - t, 2)
        }

        # ==========================
        # Gold Layer
        # ==========================

        logger.info("[3/4] Running Gold Layer...")

        t = time.time()

        run_gold_layer()

        execution_report["Gold"] = {
            "status": "SUCCESS",
            "duration_seconds": round(time.time() - t, 2)
        }

        # ==========================
        # Charts
        # ==========================

        logger.info("[4/4] Generating Charts...")

        t = time.time()

        generate_visualizations()

        execution_report["Charts"] = {
            "status": "SUCCESS",
            "duration_seconds": round(time.time() - t, 2)
        }

    except Exception:

        pipeline_status = "FAILED"

        logger.exception("Pipeline Failed")

    finally:

        total_time = round(time.time() - start_time, 2)

        report = {
            "pipeline": "RetailPulse",
            "execution_time": datetime.now().isoformat(),
            "status": pipeline_status,
            "total_duration_seconds": total_time,
            "steps": execution_report
        }

        report_path = os.path.join(
            BASE_DIR,
            "data",
            "pipeline_run_report.json"
        )

        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)

        logger.info("=" * 60)
        logger.info(f"Pipeline Status : {pipeline_status}")
        logger.info(f"Execution Time : {total_time} seconds")
        logger.info(f"Report Saved : {report_path}")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()