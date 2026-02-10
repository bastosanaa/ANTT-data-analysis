import os

from pyspark.sql import SparkSession

from extract import ExcelExtractor
from transform import SparkTransformer
from load import DataModeler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, 'data', 'DR2025-MRS.xlsx')
TEMP_DIR = os.path.join(BASE_DIR, 'data', 'temp')
DB_PATH = os.path.join(BASE_DIR, 'data', 'antt.db')


def start_spark():
    return SparkSession.builder \
        .appName("ETL_Ferrovias_OO") \
        .master("local[*]") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()

def main():
    print("--- INICIANDO PIPELINE DE DADOS (POO) ---")

    extractor = ExcelExtractor(EXCEL_FILE, TEMP_DIR)
    csv_paths = extractor.run()

    if not csv_paths:
        print("Pipeline abortado.")
        return

    spark = start_spark()

    try:
        transformer = SparkTransformer(spark)
        dfs_clean = transformer.run(csv_paths)

        loader = DataModeler(DB_PATH)
        loader.run(dfs_clean)

    finally:
        spark.stop()
        print("--- PIPELINE FINALIZADO ---")

if __name__ == "__main__":
    main()