# Spotilight

## Introduction
This project builds an ETL (Extract, Transform, Load) process using the Spotify API to extract listening data, transform it using Python and PySpark, and load it into a PostgreSQL database. Additionally, a periodic summary email is generated using SQL and Python, which includes metrics like total listening time, top artists, frequently listened songs, etc.

## Project Goals & Objectives
The main goal is to create a system that:
- Automatically extracts listening data from the Spotify API (Spotipy).
- Transforms the data into Spark dataframes using Python.
- Loads the data into a PostgreSQL database.
- Generates a summary email with relevant metrics.
- Automates the entire process using Celery.

## Project Scope
- Extract data from the Spotify API.
- Transform data using Python and PySpark.
- Load data into a PostgreSQL database.
- Generate periodic summary emails with user-specific listening metrics.
- Extend the analysis to provide monthly or yearly summaries using machine learning for enhanced user experience.

## Project Limitations & Constraints
- Only user-specific data can be retrieved using the Spotify API.
- Limited memory due to data storage in a PostgreSQL database, making the application less scalable.

## Feasibility Study
Based on available resources and technology, this project is feasible. The Spotify API provides an interface for extracting listening data, and Python with Pandas offers powerful tools for data transformation and loading. Celery enables process automation, enhancing efficiency and reliability.

## System Requirement Specifications

### Hardware Specifications
- **Operating System**: Windows 11, 64-bit
- **RAM**: 8 GB

### Software Specifications
- **Software**:
  - Java SE 8 or above
  - Python 3.8 or above
  - PostgreSQL 15
  - pgAdmin 4
  - Spark 3.3.2
  - Hadoop (winutil.exe)
  - Redis 3.0.5
  - VS Code
  - PostgreSQL JDBC Driver (postgresql-42.6.0.jar)

- **Python Libraries**:
  - `pyspark`
  - `spotipy` (Spotify API)
  - `celery`
  - `psycopg2`
  - `tabulate`
  - `datetime`
  - `tabulate`

## Project Structure

```
/Spotify-ETL-Project
│
├── /scripts
│   ├── extract_transform_data.py
│   ├── load.py
│   ├── send_mail.py
│   └── tasks.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

## Usage

1. Run requirements.txt file.
   ```bash
   pip install -r requirements.txt
   ```
2. Run the ETL scripts to extract, transform, and load data.
    ```bash
    python scripts/extract_data.py
    python scripts/transform_data.py
    python scripts/load_data.py
    ```
3. Generate the summary email.
    ```bash
    python scripts/tasks.py
    ```
4. Automate the ETL process using Celery.
    ```bash
    celery -A tasks worker --loglevel=info
    ```
