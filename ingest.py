# ingest.py
import os
import boto3
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from botocore.exceptions import ClientError

# Load env vars
s3_bucket = os.getenv("S3_BUCKET")
csv_key = os.getenv("CSV_KEY")
rds_host = os.getenv("RDS_HOST")
rds_user = os.getenv("RDS_USER")
rds_pass = os.getenv("RDS_PASS")
rds_db = os.getenv("RDS_DB")
rds_table = os.getenv("RDS_TABLE")
glue_db = os.getenv("GLUE_DB")
glue_table = os.getenv("GLUE_TABLE")
s3_location = os.getenv("S3_LOCATION")

def read_from_s3():
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=s3_bucket, Key=csv_key)
    return pd.read_csv(obj['Body'])

def push_to_rds(df):
    try:
        engine = create_engine(f"mysql+pymysql://{rds_user}:{rds_pass}@{rds_host}/{rds_db}")
        df.to_sql(rds_table, engine, if_exists="replace", index=False)
        print("✅ Data uploaded to RDS.")
    except Exception as e:
        print(f"❌ RDS upload failed: {e}")
        raise

def fallback_to_glue():
    try:
        glue = boto3.client("glue")
        glue.create_database(DatabaseInput={'Name': glue_db})
        glue.create_table(
            DatabaseName=glue_db,
            TableInput={
                'Name': glue_table,
                'StorageDescriptor': {
                    'Columns': [
                        {'Name': 'column1', 'Type': 'string'},
                        {'Name': 'column2', 'Type': 'string'}
                    ],
                    'Location': s3_location,
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                        'Parameters': {'field.delim': ','}
                    }
                },
                'TableType': 'EXTERNAL_TABLE'
            }
        )
        print("✅ Fallback to AWS Glue successful.")
    except ClientError as e:
        print(f"❌ Glue fallback failed: {e}")

if __name__ == "__main__":
    df = read_from_s3()
    try:
        push_to_rds(df)
    except:
        fallback_to_glue()

