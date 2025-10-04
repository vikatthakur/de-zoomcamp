# setup Java environment for Spark
# This is for Windows OS
# import os

# os.environ["JAVA_HOME"] = r"C:\\Program Files\\Java\\jdk1.8.0_202"
# os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ["PATH"]

# create local spark session
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format
from pyspark.sql.types import TimestampType
from sqlalchemy import create_engine
from time import time

import pandas as pd
import os
import argparse


def main(params):
    ''''
    # Example credentials
        username = "root"
        password = "root"
        host = "localhost"
        port = 5432
        database = "ny_taxi"
        url = ${url}
        table = "yellow_taxi_trips"
    '''
    start_time = time()
    username = params.username
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    url = params.url
    table = params.table

    output_file_path = "data/output.parquet"

    # download parquet file
    os.system(
        f"wget {url} -O {output_file_path}"
    )

    spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("etl-postgres-1")
    .config("spark.jars", "postgresql-42.7.4.jar")
    .config("spark.driver.extraJavaOptions", "-Duser.timezone=Asia/Kolkata")
    .config("spark.executor.extraJavaOptions", "-Duser.timezone=Asia/Kolkata")
    .getOrCreate()
)
    df = spark.read.parquet(output_file_path)

    print("Row count for downloaded file:", df.count())
    df.printSchema()

    # Write directly to Postgres via JDBC
    df.write \
      .format("jdbc") \
      .option("url", f"jdbc:postgresql://{host}:{port}/{database}") \
      .option("dbtable", table) \
      .option("user", username) \
      .option("password", password) \
      .option("driver", "org.postgresql.Driver") \
      .mode("overwrite") \
      .save()

    
    print("All data inserted successfully")
    end_time = time()
    print("Total time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":

#argparse all above parameters
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--username", help="username for postgres", default="root")
    argparser.add_argument("--password", help="password for postgres", default="root")
    argparser.add_argument("--host", help="host for postgres", default="localhost")
    argparser.add_argument("--port", help="port for postgres", default=5432)
    argparser.add_argument("--database", help="database for postgres", default="ny_taxi")
    argparser.add_argument("--url", help="data url", default="")
    argparser.add_argument("--table", help="table name", default="yellow_taxi_trips")
    args = argparser.parse_args()
    main(args)

