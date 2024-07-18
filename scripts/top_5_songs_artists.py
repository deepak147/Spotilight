def top_5_songs_artists(cur):
    
    top_songs_art_played = [["Song Name", "Arist Name", "Times Played"]]
    cur.callproc("spotify.function_last_7_days_songs_artist_played")
    for row in cur.fetchall():
        song_name = row[0]
        artist_name = row[1]
        times_played = int(row[2])
        element = [song_name, artist_name, times_played]
        top_songs_art_played.append(element)
        
    return top_songs_art_played