music_queue = ["url1", "url2", "url3"]
print(music_queue)

for i in music_queue:
	music_queue.pop(0)
	print(music_queue)

if not music_queue:
	print("não tem")
else:
	print("tem elementos")