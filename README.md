# 🚀 Data Ingestion from S3 to RDS with Fallback to AWS Glue

This project demonstrates a Dockerized Python application that automates a data pipeline for reading CSV data from Amazon S3, inserting it into an RDS (MySQL-compatible) database, and falling back to AWS Glue Data Catalog in case of RDS failure.

---

## 📌 Objective

- Read a CSV file from an Amazon S3 bucket
- Parse the CSV using `pandas`
- Upload data to an RDS MySQL-compatible database
- If the RDS upload fails, create a fallback table in AWS Glue Data Catalog pointing to the S3 location

---

## 🛠️ Technologies Used

- **AWS Services**: S3, RDS, Glue, IAM
- **Python Libraries**: boto3, pandas, SQLAlchemy, PyMySQL
- **Docker**: For containerizing the application

---

## 📁 Project Structure

data-ingestion-s3-rds-glue/
│
├── ingest_data.py # Main Python script
├── requirements.txt # Python dependencies
├── Dockerfile # Docker image definition
├── README.md # Project documentation
└── assets/ # (Optional) Screenshots folder

## ✅ Prerequisites

- AWS account with programmatic access (Access Key + Secret)
- S3 bucket with a sample CSV file
- RDS (MySQL) instance with an open port
- AWS Glue permissions to create database and tables
- Docker installed on your machine

---

## ⚙️ Configuration (Environment Variables)

Pass these values while running the Docker container:

| Variable Name       | Description                          |
|---------------------|--------------------------------------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key                  |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key              |
| `AWS_DEFAULT_REGION` | AWS region (e.g., ap-south-1)       |
| `S3_BUCKET`         | Name of the S3 bucket                |
| `S3_KEY`            | CSV file key in S3                   |
| `RDS_HOST`          | RDS endpoint                         |
| `RDS_USER`          | RDS username                         |
| `RDS_PASSWORD`      | RDS password                         |
| `RDS_DB`            | RDS database name                    |
| `RDS_TABLE`         | Target table in RDS                  |
| `GLUE_DB`           | Glue database name                   |
| `GLUE_TABLE`        | Glue table name                      |
| `GLUE_S3_LOCATION`  | S3 path for Glue table               |

---

## 🐳 Docker Instructions

### Build the Docker image

```bash
docker build -t data-ingestion-app .

Run the container

docker run --rm \
-e AWS_ACCESS_KEY_ID=your-access-key \
-e AWS_SECRET_ACCESS_KEY=your-secret-key \
-e AWS_DEFAULT_REGION=ap-south-1 \
-e S3_BUCKET=your-bucket-name \
-e S3_KEY=data.csv \
-e RDS_HOST=mydb.xxxxxx.ap-south-1.rds.amazonaws.com \
-e RDS_USER=admin \
-e RDS_PASSWORD=yourpassword \
-e RDS_DB=mydatabase \
-e RDS_TABLE=ingested_data \
-e GLUE_DB=glue_database \
-e GLUE_TABLE=glue_table \
-e GLUE_S3_LOCATION=s3://your-bucket-name/data/ \
data-ingestion-app
