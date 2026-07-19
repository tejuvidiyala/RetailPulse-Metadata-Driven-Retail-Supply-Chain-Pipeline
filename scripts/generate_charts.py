import sys
import os

# Allow importing utils.py from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_config, setup_logger


def generate_visualizations():

    config = load_config()
    logger = setup_logger()

    logger.info("Generating Visualization Charts...")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    gold_dir = os.path.join(BASE_DIR, "data", "gold")
    output_dir = os.path.join(BASE_DIR, "outputs")

    os.makedirs(output_dir, exist_ok=True)

    # Seaborn Style
    sns.set_theme(style="whitegrid")

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 13,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.titlesize": 14
    })

    # -------------------------------------------------------
    # 1. Top Products
    # -------------------------------------------------------

    top_products_path = os.path.join(gold_dir, "top_products.csv")

    if os.path.exists(top_products_path):

        try:

            logger.info("Generating Top Products Chart...")

            df = pd.read_csv(top_products_path)

            df = df.sort_values(
                by="total_revenue",
                ascending=True
            )

            plt.figure(figsize=(10,6))

            bars = plt.barh(
                df["product_name"],
                df["total_revenue"],
                color=sns.color_palette("plasma", len(df))
            )

            for bar in bars:

                width = bar.get_width()

                plt.text(
                    width,
                    bar.get_y()+bar.get_height()/2,
                    f"₹{width:,.0f}",
                    va="center",
                    fontsize=9
                )

            plt.title("Top 10 Products by Revenue")
            plt.xlabel("Revenue")
            plt.ylabel("Products")

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    output_dir,
                    "top_10_products_revenue.png"
                ),
                dpi=300
            )

            plt.close()

        except Exception as e:
            logger.error(e)

    # -------------------------------------------------------
    # 2. Daily Revenue
    # -------------------------------------------------------

    daily_sales_path = os.path.join(gold_dir, "daily_sales.csv")

    if os.path.exists(daily_sales_path):

        try:

            logger.info("Generating Daily Revenue Chart...")

            df = pd.read_csv(daily_sales_path)

            df["date"] = pd.to_datetime(df["date"])

            plt.figure(figsize=(12,5))

            plt.plot(
                df["date"],
                df["total_revenue"],
                marker="o",
                linewidth=2
            )

            plt.fill_between(
                df["date"],
                df["total_revenue"],
                alpha=0.2
            )

            plt.title("Daily Revenue Trend")

            plt.xlabel("Date")
            plt.ylabel("Revenue")

            plt.xticks(rotation=45)

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    output_dir,
                    "daily_revenue_trend.png"
                ),
                dpi=300
            )

            plt.close()

        except Exception as e:
            logger.error(e)

    # -------------------------------------------------------
    # 3. Store Performance
    # -------------------------------------------------------

    store_path = os.path.join(
        gold_dir,
        "store_performance.csv"
    )

    if os.path.exists(store_path):

        try:

            logger.info("Generating Store Performance Chart...")

            df = pd.read_csv(store_path)

            plt.figure(figsize=(10,6))

            bars = plt.bar(
                df["store_name"],
                df["total_revenue"],
                color=sns.color_palette("viridis", len(df))
            )

            for bar in bars:

                h = bar.get_height()

                plt.text(
                    bar.get_x()+bar.get_width()/2,
                    h,
                    f"₹{h:,.0f}",
                    ha="center",
                    fontsize=8
                )

            plt.xticks(rotation=30)

            plt.title("Store Performance by Revenue")

            plt.xlabel("Store")

            plt.ylabel("Revenue")

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    output_dir,
                    "store_revenue_performance.png"
                ),
                dpi=300
            )

            plt.close()

        except Exception as e:
            logger.error(e)

    logger.info("Charts generated successfully!")


if __name__ == "__main__":
    generate_visualizations()