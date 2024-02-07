import requests
import os
import json
from dotenv import load_dotenv
from random import randint

load_dotenv()

# set the apikey and limit
apikey = os.getenv("TENOR_API")  # click to set to your apikey
lmt = 8
ckey = os.getenv("CLIENT_KEY")  # set the client_key for the integration and use the same value for all API calls

def get_gif_pokemon(term):
	# get the top 8 GIFs for the search term
	r = requests.get(
		"https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (term, apikey, ckey,  lmt))

	if r.status_code == 200:
		# load the GIFs using the urls for the smaller GIF sizes
		top_8gifs = json.loads(r.content)
		#print(top_8gifs)
	else:
		top_8gifs = None

	return top_8gifs["results"][randint(0,7)]["url"]

if __name__ == "__main__":
	get_gif_pokemon("Charmander")
