import logging
import psycopg2
import sys

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

from extract_transform_data import extract_transform
from load import load
from send_mail import send_mail
from spark_session import spark_session
from spotify_auth import authenticate_spotify
from top_5_songs_duration import top_5_songs_duration
from total_time import total_time
from top_5_songs_artists import top_5_songs_artists
from top_artists import top_artists


app = Celery("tasks", broker="redis://localhost:6379/0")
logger = get_task_logger(__name__)
file_handler = logging.FileHandler('spotify_etl.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
load_dotenv()


@app.task
def spotify_etl_func():
    spark = spark_session()

    try:  # Authenticate with Spotify API
        recently_played = authenticate_spotify()
        logger.info("User data successfully retrieved")

        if len(recently_played) == 0:
            logger.warning("No results received from Spotify")
            sys.exit("No results received from Spotify")

    except Exception as e:
        logger.error(f"Error while authenticating with Spotify API: {e}")
        sys.exit(f"Error while authenticating with Spotify API: {e}")

    df_list = extract_transform(recently_played, spark)

    try:
        load(df_list)

    except Exception as e:
        logger.error(f"Error while loading data into postgres tables: {e}")
        sys.exit(f"Error while loading data into postgres tables: {e}")


@app.task
def weekly_mail_func():
    try:
        conn = psycopg2.connect(
            host="localhost", dbname="spotify", user="postgres", password="admin"
        )
        cur = conn.cursor()
        logger.info("Successfully connected to postgres database")

    except Exception as e:
        logger.error(f"Error while connecting to database: {e}")
        sys.exit(f"Error while connecting to database: {e}")

    try:
        # Top 5 Songs by Time Listened (MIN)
        top_5_songs_min = top_5_songs_duration(cur)

        logger.info(
            "Successfully retrieved top 5 songs listened wrt to minutes played"
        )

    except Exception as e:
        logger.error(
            f"Error retrieving top 5 songs listened wrt to minutes played: {e}"
        )
        sys.exit(f"Error retrieving top 5 songs listened wrt to minutes played: {e}")

    try:
        # Total Time Listened (HOURS)
        total_time_listened_hrs = total_time(cur)

        logger.info("Successfully retrieved total time spent")

    except Exception as e:
        logger.error(f"Error while retrieving total time spent: {e}")
        sys.exit(f"Error while retrieving total time spent: {e}")

    try:
        # Top 5 Songs and Artists by Times Played
        top_songs_art_played = top_5_songs_artists(cur)

        logger.info("Successfully retrieved top 5 songs and artists")

    except Exception as e:
        logger.error(f"Error while retrieving top 5 songs and artists: {e}")
        sys.exit(f"Error while retrieving top 5 songs and artists: {e}")

    try:
        # Top Artists Played
        top_art_played = top_artists(cur)

        logger.info("Successfully retrieved top artists")

    except Exception as e:
        logger.error(f"Error while retrieving top artists: {e}")
        sys.exit(f"Error while retrieving top artists: {e}")

    try:
        send_mail(top_5_songs_min, total_time_listened_hrs, top_songs_art_played, top_art_played)

        logger.info("Successfully sent the mail")

    except Exception as e:
        logger.error(f"Error while sending mail: {e}")
        sys.exit(f"Error while sending mail: {e}")


app.conf.beat_schedule = {
    "spotify_etl_task": {
        "task": "tasks.spotify_etl_func",
        "schedule": crontab(hour='10', minute='0'),
    },
    "weekly_mail_task": {
        "task": "tasks.weekly_mail_func",
        "schedule": crontab(hour='10', minute='10'),
    },
}

app.conf.timezone = "America/Chicago"
if __name__ == "__main__":
    app.start()
