CREATE TABLE IF NOT EXISTS spotify_schema.spotify_track(
    Unique_identifier TEXT PRIMARY KEY NOT NULL,
    Song_id TEXT NOT NULL,
    Song_name TEXT,
    Duration_ms INTEGER,
    url TEXT,
    popularity SMALLINT,
    date_time_played TIMESTAMP,
    album_id TEXT,
    artist_id TEXT,
    date_time_inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


CREATE TABLE IF NOT EXISTS spotify_schema.spotify_album(
    Album_id TEXT NOT NULL PRIMARY KEY,
    Name TEXT,
    Release_date TEXT,
    Total_tracks SMALLINT,
    url TEXT
    );


CREATE TABLE IF NOT EXISTS spotify_schema.spotify_artists(
    Artist_id TEXT PRIMARY KEY NOT NULL,
    Name TEXT,
    url TEXT);
