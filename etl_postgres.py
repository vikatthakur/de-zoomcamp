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
    '''

    username = params.username
    password = params.password
    host = params.host
    port = params.port
    database = params.database

    output_file_path = "data/output.parquet"

    #download the from os wget command
    os.system(f"wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-02.parquet -O {output_file_path}"
    )

    spark = SparkSession.builder.master("local[*]").appName("etl-postgres-1").getOrCreate()

    # read the parquet data from /data folder into a dataframe
    df = spark.read.parquet(output_file_path)

    # Convert timestamp columns to string first
    timestamp_cols = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]
    for c in timestamp_cols:
        df = df.withColumn(c, date_format(col(c), "yyyy-MM-dd HH:mm:ss"))

    # volume of data
    print("Row count for downloaded file:", df.count())

    # data showcase/ schema showcase
    df.printSchema()

    # convert to pandas
    pdf = df.toPandas()
    for c in timestamp_cols:
        pdf[c] = pd.to_datetime(pdf[c])

    # Create the engine
    engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")
    engine.connect()

    create_statement_postgres = pd.io.sql.get_schema(pdf, name="yellow_tax_data", con=engine)
    print(create_statement_postgres)

    # creating and inserting data in yellow_taxi_trips
    # create yellow_taxi_trips
    table_name = "yellow_taxi_trips"
    df_head = pdf.head(0)
    df_head.to_sql(name=table_name, con=engine, if_exists="append")

    # insert chunks of 10000

    chunksize = 10000
    for i in range(0, len(pdf), chunksize):
        t_start = time()
        pdf.iloc[i:i+chunksize].to_sql(name=table_name, con=engine, if_exists="append")
        t_end = time()
        print(f"Inserted data successfully in {t_end - t_start:.3f}s")
    print("All data inserted successfully")





if __name__ == "__main__":

#argparse all above parameters
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--username", help="username for postgres", default="root")
    argparser.add_argument("--password", help="password for postgres", default="root")
    argparser.add_argument("--host", help="host for postgres", default="localhost")
    argparser.add_argument("--port", help="port for postgres", default=5432)
    argparser.add_argument("--database", help="database for postgres", default="ny_taxi")
    args = argparser.parse_args()
    main(args)

