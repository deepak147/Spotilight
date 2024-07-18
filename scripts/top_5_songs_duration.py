def top_5_songs_duration(cur):

    # Top 5 Songs by Time Listened (MIN)
    top_5_songs_min = [["Song Name", "Time (Min)"]]
    cur.callproc("spotify.function_last_7_days_top_5_songs_duration")
    for row in cur.fetchall():
        song_name = row[0]
        min_listened = float(row[1])
        element = [song_name, min_listened]
        top_5_songs_min.append(element)
        
    return top_5_songs_min