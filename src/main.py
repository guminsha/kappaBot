import os
from dotenv import load_dotenv
from commands import bot

load_dotenv()

bot.run(os.getenv('TOKEN'))