def load(df_list):
    
    album_df = df_list[0]
    artist_df = df_list[1]
    song_df = df_list[2]
    
    song_df.write.format("jdbc").option(
        "url", "jdbc:postgresql://localhost:5432/spotify"
    ).option("dbtable", "spotify.track").option("user", "postgres").option(
        "password", "admin"
    ).option(
        "truncate", "true"
    ).mode(
        "overwrite"
    ).save()

    album_df.write.format("jdbc").option(
        "url", "jdbc:postgresql://localhost:5432/spotify"
    ).option("dbtable", "spotify.album").option("user", "postgres").option(
        "password", "admin"
    ).option(
        "truncate", "true"
    ).mode(
        "overwrite"
    ).save()

    artist_df.write.format("jdbc").option(
        "url", "jdbc:postgresql://localhost:5432/spotify"
    ).option("dbtable", "spotify.artists").option("user", "postgres").option(
        "password", "admin"
    ).option(
        "truncate", "true"
    ).mode(
        "overwrite"
    ).save()