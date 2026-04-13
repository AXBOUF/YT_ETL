import video_stats

# 1. Define the handle you want to look up
handle = "bbacalhau"

# 2. Call the function from the imported module
playlist_id = video_stats.get_channel_playlist_id(handle)

# 3. Use the result
print(f"The Playlist ID is: {playlist_id}")
