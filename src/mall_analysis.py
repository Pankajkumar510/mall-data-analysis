"""Reusable PySpark analysis functions for PRCE-003 Mall Customers."""

from pathlib import Path
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def standardize_columns(df: DataFrame) -> DataFrame:
    """Trim column names and replace spaces/special punctuation with underscores."""
    import re
    renamed = df
    for old in df.columns:
        new = re.sub(r"[^0-9a-zA-Z]+", "_", old.strip()).strip("_")
        renamed = renamed.withColumnRenamed(old, new)
    return renamed


def inspect_data(df: DataFrame) -> None:
    print(f"Rows: {df.count():,}")
    print(f"Columns ({len(df.columns)}): {df.columns}")
    df.printSchema()
    df.show(10, truncate=False)
    print("Null counts:")
    df.select([
        F.count(F.when(F.col(c).isNull(), c)).alias(c)
        for c in df.columns
    ]).show(truncate=False)
    print(f"Duplicate rows: {df.count() - df.dropDuplicates().count():,}")


def spending_score_summary(df: DataFrame, score_col: str = "Spending_Score"):
    """Return descriptive statistics and Low/Medium/High group summary."""
    if score_col not in df.columns:
        raise ValueError(
            f"Required spending score column '{score_col}' not found. "
            f"Available columns: {df.columns}"
        )

    numeric = df.withColumn(score_col, F.col(score_col).cast("double"))
    stats = numeric.select(
        F.count(score_col).alias("non_null_count"),
        F.mean(score_col).alias("mean"),
        F.expr(f"percentile_approx({score_col}, 0.5)").alias("median"),
        F.stddev(score_col).alias("stddev"),
        F.min(score_col).alias("minimum"),
        F.max(score_col).alias("maximum"),
    )

    grouped = (
        numeric
        .withColumn(
            "Spending_Group",
            F.when(F.col(score_col).between(1, 39), "Low (1-39)")
             .when(F.col(score_col).between(40, 60), "Medium (40-60)")
             .when(F.col(score_col).between(61, 100), "High (61-100)")
             .otherwise("Outside expected range")
        )
        .groupBy("Spending_Group")
        .agg(F.count("*").alias("Customer_Count"))
        .withColumn(
            "Percentage",
            F.round(F.col("Customer_Count") * 100.0 / F.sum("Customer_Count").over(
                __import__("pyspark").sql.Window.partitionBy()
            ), 2)
        )
        .orderBy("Spending_Group")
    )
    return numeric, stats, grouped


def optional_segment_summaries(df: DataFrame):
    results = {}
    if "Gender" in df.columns and "Spending_Score" in df.columns:
        results["gender"] = (
            df.groupBy("Gender")
            .agg(
                F.count("*").alias("Customer_Count"),
                F.round(F.avg("Spending_Score"), 2).alias("Average_Spending_Score"),
                F.expr("percentile_approx(Spending_Score, 0.5)").alias("Median_Spending_Score")
            )
            .orderBy("Gender")
        )
    if "Age" in df.columns and "Spending_Score" in df.columns:
        age = df.withColumn(
            "Age_Group",
            F.when(F.col("Age") < 25, "Under 25")
             .when(F.col("Age") < 35, "25-34")
             .when(F.col("Age") < 45, "35-44")
             .when(F.col("Age") < 55, "45-54")
             .otherwise("55+")
        )
        results["age"] = (
            age.groupBy("Age_Group")
            .agg(
                F.count("*").alias("Customer_Count"),
                F.round(F.avg("Spending_Score"), 2).alias("Average_Spending_Score")
            )
            .orderBy("Age_Group")
        )
    if "Annual_Income_k" in df.columns and "Spending_Score" in df.columns:
        results["income"] = df.select("Annual_Income_k", "Spending_Score")
    return results
