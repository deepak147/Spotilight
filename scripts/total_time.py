def total_time(cur):
    
    cur.callproc("spotify.function_last_7_days_hrs_listened")
    total_time_listened_hrs = float(cur.fetchone()[0])
    
    return total_time_listened_hrs