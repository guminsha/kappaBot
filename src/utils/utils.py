import os
import asyncio
from youtubesearchpython import VideosSearch

def delete_queue(queue):
	for title in queue:
		delete_music(title)

def delete_music(title):
	path = f"src/assets/audios/{title}.mp3"
	if os.path.exists(path):
		print(f"Deleting {title}.mp3")
		os.remove(path)

def get_video_url_by_title(title):
    videos_search = VideosSearch(title, limit = 1)
    results = videos_search.result()['result']
    if results:
        return results[0]["link"]
    else:
        return None
	
async def delete_message(msg):
	await asyncio.sleep(20)
	await msg.delete()

if __name__ == "__main__":
	print(get_video_url_by_title("numb linkin park"))