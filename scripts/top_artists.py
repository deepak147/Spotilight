def top_artists(cur):
    
    top_art_played = [["Artist Name", "Times Played"]]
    cur.callproc("spotify.function_last_7_days_artist_played")
    for row in cur.fetchall():
        artist_name = row[0]
        times_played = int(row[1])
        element = [artist_name, times_played]
        top_art_played.append(element)
        
    return top_art_played