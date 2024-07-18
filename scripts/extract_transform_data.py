import logging
import sys
from pyspark.sql.functions import (
    from_unixtime,
    unix_timestamp,
    concat,
    lit,
    to_timestamp,
)

logging.basicConfig(filename='spotify_etl.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger()

def extract_transform(recently_played, spark):
    
    try:  # Extract album data
        album_list = []
        for row in recently_played["items"]:
            album_id = row["track"]["album"]["id"]
            album_name = row["track"]["album"]["name"]
            album_release_date = row["track"]["album"]["release_date"]
            album_total_tracks = row["track"]["album"]["total_tracks"]
            album_url = row["track"]["album"]["external_urls"]["spotify"]
            album_element = {
                "album_id": album_id,
                "name": album_name,
                "release_date": album_release_date,
                "total_tracks": album_total_tracks,
                "url": album_url,
            }
            album_list.append(album_element)

        album_df = spark.createDataFrame(album_list).dropDuplicates(["album_id"])

    except Exception as e:
        logger.error(f"Error while extracting album data: {e}")
        sys.exit(f"Error while extracting album data: {e}")

    try:  # Extract artist data
        artist_list = []
        id_list = []
        name_list = []
        url_list = []
        for item in recently_played["items"]:
            for key, value in item.items():
                if key == "track":
                    for data_point in value["artists"]:
                        id_list.append(data_point["id"])
                        name_list.append(data_point["name"])
                        url_list.append(data_point["external_urls"]["spotify"])
                        artist_element = {
                            "artist_id": data_point["id"],
                            "name": data_point["name"],
                            "url": data_point["external_urls"]["spotify"],
                        }
                        artist_list.append(artist_element)

        artist_df = spark.createDataFrame(artist_list).dropDuplicates(["artist_id"])

    except Exception as e:
        logger.error(f"Error while extracting artist data: {e}")
        sys.exit(f"Error while extracting artist data: {e}")

    try:  # Extract songs data
        song_list = []
        for row in recently_played["items"]:
            song_id = row["track"]["id"]
            song_name = row["track"]["name"]
            song_duration = row["track"]["duration_ms"]
            song_url = row["track"]["external_urls"]["spotify"]
            song_time_played = row["played_at"]
            album_id = row["track"]["album"]["id"]
            artist_id = row["track"]["album"]["artists"][0]["id"]
            song_element = {
                "song_id": song_id,
                "song_name": song_name,
                "duration_ms": song_duration,
                "url": song_url,
                "date_time_played": song_time_played,
                "album_id": album_id,
                "artist_id": artist_id,
                "UNIX_Time_Stamp": "",
                "unique_identifier": "",
            }
            song_list.append(song_element)
        song_df = spark.createDataFrame(song_list)
        spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")
        song_df = song_df.withColumn(
            "date_time_played",
            unix_timestamp("date_time_played", "yyyy-MM-dd'T'HH:mm:ss"),
        )
        song_df = song_df.withColumn(
            "date_time_played", from_unixtime("date_time_played", "yyyy-MM-dd HH:mm:ss")
        )
        song_df = song_df.withColumn(
            "date_time_played", to_timestamp("date_time_played")
        )
        print(song_df.show())
        print(song_df.printSchema())
        song_df = song_df.withColumn(
            "UNIX_Time_Stamp",
            (
                unix_timestamp("date_time_played", "yyyy-MM-dd HH:mm:ss")
                - unix_timestamp(lit("1970-01-01"), "yyyy-MM-dd")
            )
            / lit(1),
        )
        song_df = song_df.withColumn(
            "unique_identifier",
            concat(song_df.song_id, lit("-"), song_df.UNIX_Time_Stamp.cast("string")),
        )
        song_df = song_df[
            [
                "unique_identifier",
                "song_id",
                "song_name",
                "duration_ms",
                "url",
                "date_time_played",
                "album_id",
                "artist_id",
            ]
        ]

    except Exception as e:
        logger.error(f"Error while extracting songs data: {e}")
        sys.exit(f"Error while extracting songs data: {e}")
        
    return [album_df, artist_df, song_df]