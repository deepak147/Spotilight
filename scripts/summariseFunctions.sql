--Top songs based on duration
CREATE FUNCTION function_last_7_days_top_5_songs_duration() 
Returns TABLE (song_name text, min_duration decimal) language plpgsql AS $$ 
BEGIN 
  RETURN query 
  SELECT   st.song_name, 
           Round(sum(cast(duration_ms AS decimal)/60000),2) AS min_duration 
  FROM     spotify_track                                    AS st 
  WHERE    date_time_played > CURRENT_DATE – interval ‘7 days’ 
  GROUP BY st.song_name 
  ORDER BY min_duration DESC limit 5; 

--Total time listened
CREATE FUNCTION function_last_7_days_hrs_listened() 
RETURNS TABLE (total_time_listened_hrs decimal) LANGUAGE plpgsql AS $$ 
BEGIN 
  RETURN query 
  SELECT   ROUND(SUM(CAST (st.duration_ms AS decimal)/3600000),2) AS total_time_listened_hrs 
  FROM     spotify_schema.spotify_track AS st 
  WHERE    date_time_played > CURRENT_DATE – INTERVAL ‘7 days’;
End;$$ 

--Top songs and artists
CREATE FUNCTION function_last_7_days_songs_artist_played() 
RETURNS TABLE (song_name TEXT, artist_name TEXT, times_played INT) LANGUAGE plpgsql AS $$ 
BEGIN 
  RETURN query 
  SELECT st.song_name, sa.name AS artist_name,COUNT(st.*)::INT AS times_played
    FROM spotify_track AS st
    INNER JOIN spotify_artists AS sa 
    ON st.artist_id = sa.artist_id
    WHERE date_time_played > CURRENT_DATE – INTERVAL ‘7 days’
    GROUP BY st.song_name, sa.name
    ORDER BY times_played DESC
    LIMIT 5;

---Top artists
CREATE FUNCTION function_last_7_days_artist_played() 
RETURNS TABLE (name TEXT, number_plays INT) LANGUAGE plpgsql AS $$ 
BEGIN 
  RETURN query 
 SELECT art.name, COUNT(track.*):: INT AS number_plays
    FROM spotify_schema.spotify_track AS track
    INNER JOIN spotify_schema.spotify_artists AS art ON track.artist_id=art.artist_id
    WHERE date_time_played > CURRENT_DATE – INTERVAL ‘7 days’
    GROUP BY art.name
    ORDER BY number_plays DESC
    LIMIT 5;
End;$$ 

