import findspark
from pyspark.sql import SparkSession

def spark_session():
    
    findspark.init()  # Initialize Spark
    spark = (
        SparkSession.builder.appName("spotify_etl")
        .config("spark.driver.extraClassPath", "./postgresql-42.6.0.jar")
        .config(
            "spark.sql.catalog.postgres", "org.apache.spark.sql.jdbc.CatalogBuilder"
        )
        .config(
            "spark.sql.catalog.postgres.url", "jdbc:postgresql://localhost:5432/spotify"
        )
        .config("spark.sql.catalog.postgres.username", "postgres")
        .config("spark.sql.catalog.postgres.password", "admin")
        .getOrCreate()
    )
    
    return spark