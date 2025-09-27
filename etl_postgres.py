# setup Java environment for Spark
# This is for Windows OS
# import os

# os.environ["JAVA_HOME"] = r"C:\\Program Files\\Java\\jdk1.8.0_202"
# os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ["PATH"]

# create local spark session
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format
from pyspark.sql.types import TimestampType

import pandas as pd

spark = SparkSession.builder.master("local[*]").appName("postgres_upload_ny_taxi").getOrCreate()

# read the parquet data from /data folder into a dataframe
df = spark.read.parquet("data/ny_taxi_data_yellow/yellow_tripdata_2021-01.parquet")

# Convert timestamp columns to string first
timestamp_cols = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]
for c in timestamp_cols:
    df = df.withColumn(c, date_format(col(c), "yyyy-MM-dd HH:mm:ss"))

# volume of data
print("Row count:", df.count())

# data showcase/ schema showcase
df.printSchema()

# convert to pandas
pdf = df.toPandas()
for c in timestamp_cols:
    pdf[c] = pd.to_datetime(pdf[c])

from sqlalchemy import create_engine
# Example credentials
username = "root"
password = "root"
host = "localhost"
port = 5432
database = "ny_taxi"

# Create the engine
engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")
engine.connect()

create_statement_postgres = pd.io.sql.get_schema(pdf, name="yellow_tax_data", con=engine)
print(create_statement_postgres)

# creating and inserting data in yellow_taxi_data
# create yellow_taxi_data
df_head = pdf.head(0)
df_head.to_sql(name="yellow_taxi_date", con=engine, if_exists="append")

# insert chunks of 10000
from time import time
chunksize = 10000
for i in range(0, len(pdf), chunksize):
    t_start = time()
    pdf.iloc[i:i+chunksize].to_sql(name="yellow_taxi_date", con=engine, if_exists="append")
    t_end = time()
    print(f"Inserted data successfully in {t_end - t_start:.3f}s")
