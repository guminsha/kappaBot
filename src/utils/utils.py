import os

def delete_queue(queue):
	for title in queue:
		delete_music(title)

def delete_music(title):
	path = f"src/assets/audios/{title}.mp3"
	if os.path.exists(path):
		print(f"Deleting {title}.mp3")
		os.remove(path)

# def play_music():
# 	voice_client.play(discord.FFmpegPCMAudio(f"src/assets/audios/{music_queue[0]}.mp3"))