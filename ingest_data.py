import os
import pandas as pd
import boto3
import pymysql
from sqlalchemy import create_engine
from botocore.exceptions import ClientError

# ENV variables
s3_bucket = os.getenv("S3_BUCKET")
s3_key = os.getenv("S3_KEY")
rds_host = os.getenv("RDS_HOST")
rds_user = os.getenv("RDS_USER")
rds_password = os.getenv("RDS_PASSWORD")
rds_db = os.getenv("RDS_DB")
rds_table = os.getenv("RDS_TABLE")
glue_db = os.getenv("GLUE_DB")
glue_table = os.getenv("GLUE_TABLE")
glue_s3_location = os.getenv("GLUE_S3_LOCATION")

# S3 download
def read_s3_csv():
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    return pd.read_csv(obj['Body'])

# RDS insert
def insert_into_rds(df):
    conn_str = f"mysql+pymysql://{rds_user}:{rds_password}@{rds_host}/{rds_db}"
    engine = create_engine(conn_str)
    df.to_sql(rds_table, con=engine, index=False, if_exists='replace')
    print("✅ Data inserted into RDS.")

# Glue fallback
def fallback_to_glue():
    glue = boto3.client('glue')
    glue.create_database(DatabaseInput={'Name': glue_db})
    glue.create_table(
        DatabaseName=glue_db,
        TableInput={
            'Name': glue_table,
            'StorageDescriptor': {
                'Columns': [{'Name': 'column1', 'Type': 'string'}, {'Name': 'column2', 'Type': 'string'}],  # update dynamically if needed
                'Location': glue_s3_location,
                'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                'SerdeInfo': {'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                              'Parameters': {'field.delim': ','}}
            },
            'TableType': 'EXTERNAL_TABLE'
        }
    )
    print("⚠️ Fallback: Table created in Glue Catalog.")

# Main
try:
    df = read_s3_csv()
    insert_into_rds(df)
except Exception as e:
    print("❌ Failed to insert into RDS:", e)
    fallback_to_glue()
