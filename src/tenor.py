import requests
import os
import json
from dotenv import load_dotenv
from random import choice

load_dotenv()

# set the apikey and limit
apikey = os.getenv("TENOR_API")  # click to set to your apikey
lmt = 5
ckey = os.getenv("CLIENT_KEY")  # set the client_key for the integration and use the same value for all API calls

def get_gif_pokemon(term):
	term = term + " Pokemon"
	# get the top 5 GIFs for the search term
	r = requests.get(f"https://tenor.googleapis.com/v2/search?q={term}&key={apikey}&client_key={ckey}&limit={lmt}"
					f"&media_filter=gif")

	if r.status_code == 200:
		# load the GIFs using the urls for the smaller GIF sizes
		top_5gifs = json.loads(r.content)
		top_5gifs = choice(top_5gifs["results"])
	else:
		top_5gifs = None
		print(r.status_code)

	return top_5gifs["media_formats"]["gif"]["url"]

if __name__ == "__main__":
	print(get_gif_pokemon("Walrein"))
