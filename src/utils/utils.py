import os

def delete_music():
	path = "src/assets/audio.mp3"
	if os.path.exists(path):
		print("Deleting audio.mp3")
		os.remove(path)
		
	