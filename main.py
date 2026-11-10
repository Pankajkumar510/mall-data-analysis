"""Run PRCE-003 Mall Customers analysis locally with PySpark."""

from pathlib import Path
import subprocess
import sys

from pyspark.sql import SparkSession
from src.mall_analysis import standardize_columns, inspect_data, spending_score_summary, optional_segment_summaries

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw"
DATA_FILE = DATA_DIR / "Mall_Customers.csv"
OUTPUT_DIR = ROOT / "output"
REPORT_DIR = ROOT / "reports"
DRIVE_ID = "1k6A8r1cCdt0Ft0mPtvnYckruaTn2XXz0"


def obtain_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        return
    print("CSV not found. Attempting Google Drive download...")
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={DRIVE_ID}"
        result = gdown.download(url, str(DATA_FILE), quiet=False)
        if not result or not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
            raise RuntimeError("Download did not produce a valid file.")
    except Exception as exc:
        raise RuntimeError(
            "Could not download the assignment dataset. Check Drive permissions, "
            "download it manually in your browser, and save it as "
            f"{DATA_FILE}. Original error: {exc}"
        )


def main():
    obtain_dataset()
    OUTPUT_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    spark = (
        SparkSession.builder
        .appName("PRCE-003-Mall-Customers")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        raw = spark.read.option("header", True).option("inferSchema", True).csv(str(DATA_FILE))
        df = standardize_columns(raw)
        print("\\n=== DATASET INSPECTION ===")
        inspect_data(df)

        # Standardize the commonly used dataset's income column name.
        if "Annual_Income_k_" in df.columns and "Annual_Income_k" not in df.columns:
            df = df.withColumnRenamed("Annual_Income_k_", "Annual_Income_k")
        if "Spending_Score_1_100" in df.columns and "Spending_Score" not in df.columns:
            df = df.withColumnRenamed("Spending_Score_1_100", "Spending_Score")

        numeric, stats, grouped = spending_score_summary(df)
        print("\\n=== SPENDING SCORE STATISTICS ===")
        stats.show(truncate=False)
        print("\\n=== SPENDING SCORE GROUPS ===")
        grouped.show(truncate=False)

        grouped.toPandas().to_csv(OUTPUT_DIR / "spending_score_group_summary.csv", index=False)
        segment_results = optional_segment_summaries(numeric)
        for name, result in segment_results.items():
            if name == "income":
                result.toPandas().to_csv(OUTPUT_DIR / "income_vs_spending_data.csv", index=False)
            else:
                result.toPandas().to_csv(OUTPUT_DIR / f"spending_by_{name}.csv", index=False)
                print(f"\\n=== SPENDING BY {name.upper()} ===")
                result.show(truncate=False)

        # Reuse report generator after actual outputs are available.
        subprocess.run(
            [sys.executable, str(ROOT / "src" / "generate_report.py")],
            check=True,
            cwd=str(ROOT)
        )
        print(f"\\nAnalysis completed. Check {OUTPUT_DIR} and {REPORT_DIR}.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
