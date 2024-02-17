import discord
from discord.ext import commands
from random import randint
import re
import openpyxl
from tenor import get_gif_pokemon
from weather import get_weather
from pytube import YouTube
import asyncio
import utils.utils as utils

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Sync bot commands with discord

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# "oi" command to make bot say hi back to who used the command

@bot.tree.command(name="oi", description="Bot te diz oi de volta")
async def hello(interaction: discord.Interaction):
    # ephemeral=True)
    await interaction.response.send_message(f"Oi, {interaction.user.mention}!")

# Make bot say something specific

@bot.tree.command(name="diga", description="Bot diz algo específico")
async def hello(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.mention} disse: {thing_to_say}!")

# Roll dice command using regex

@bot.tree.command(name="rd", description="Rola um dado de 20 lados")
async def rd(interaction: discord.Interaction, dice: str):
    pattern = re.compile("\\b([1-9][0-9]?|100)d([1-9][0-9]?|100)\\b")
    print(dice)
    print(pattern.search(dice))
    if (pattern.search(dice)):
        values_list = dice.split("d")
        dice_quantity = values_list[0]
        dice_type = values_list[1]
        list_dices = []

        for i in range(int(dice_quantity)):
            list_dices.append(randint(1, int(dice_type)))
        str_list_dices = [str(i) for i in list_dices]
        result_dices = ", ".join(str_list_dices)
        total_value_dices = sum(list_dices)

        await interaction.response.send_message(f"Você rolou {dice_quantity}d{dice_type}: {result_dices}\nTotal:({total_value_dices})")
    else:
        await interaction.response.send_message(f"Você digitou algo errado, tente algo como \"2d20\" (2 dados de 20 lados) sem aspas\nLembre-se de utilizar apenas valores entre 1 e 100", ephemeral=True)

# Excel pokemon command

workbook_pokemons = openpyxl.load_workbook("src/assets/pokemons.xlsx")["Planilha1"]
number_of_rows = 1

for row in workbook_pokemons.iter_rows(min_row=2):
    number_of_rows += 1

@bot.tree.command(name="pokemon", description="Escolhe um pokemon aleatório para você")
async def pokemon(interaction: discord.Interaction):
    pokemon_choice = randint(2, number_of_rows)
    pokemon_number = workbook_pokemons[pokemon_choice][0].value
    pokemon_gen = workbook_pokemons[pokemon_choice][1].value
    pokemon_name = workbook_pokemons[pokemon_choice][2].value
    pokemon_type = workbook_pokemons[pokemon_choice][3].value
    pokemon_info = workbook_pokemons[pokemon_choice][4].value
    pokemon_gif = get_gif_pokemon(pokemon_name)

    embed = discord.Embed()
    embed.set_image(url=pokemon_gif)
    embed.set_thumbnail(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_number.lstrip('0')}.png")
    embed.add_field(name="**Nome**:", value=pokemon_name)
    embed.add_field(name="**Nº**:", value=pokemon_number)
    embed.add_field(name="**Geração**:", value=f"{pokemon_gen}ª")
    embed.add_field(name="**Tipo**:", value=pokemon_type)
    embed.add_field(name="**Descrição**:", value=pokemon_info)

    await interaction.response.send_message(embed=embed)

# Weather bot command    

@bot.tree.command(name="tempo", description="Bot mostra previsão do tempo do local solicitado")
async def weather(interaction: discord.Interaction, city: str):
    weather = get_weather(city)
    location = weather["name"]
    description = weather["weather"][0]["description"].capitalize()
    minimum_temperature = weather["main"]["temp_min"]
    maximum_temperature = weather["main"]["temp_max"]
    feels_like = weather["main"]["feels_like"]

    await interaction.response.send_message(f"**Previsão do tempo para *{location}***\n"
                                            f"**Descrição**: {description}\n"
                                            f"**Temperatura minima**: {minimum_temperature}ºC\n"
                                            f"**Temperatura máxima**: {maximum_temperature}ºC\n"
                                            f"**Sensação térmica**: {feels_like}ºC")

# Music command

music_queue = []

@bot.tree.command(name="music", description="Music")
async def music(interaction: discord.Interaction, url: str):
    if not discord.utils.get(bot.voice_clients, guild=interaction.guild):
        channel = interaction.user.voice.channel
        voice_client = await channel.connect()
    else:
        voice_client = channel

    # Download youtube mp3 audio
    yt = YouTube(url)
    
    if yt.length > 900:
        await interaction.response.send_message("Música muito longa", delete_after=5)
        return 0
    
    await interaction.response.send_message("playing", delete_after=1)

    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename="src/assets/audio.mp3")

    # Reproduce the same audio
    voice_client.play(discord.FFmpegPCMAudio("src/assets/audio.mp3"))

    for time in range(yt.length + 1):
        print(f"{time} >> {yt.length}")
        await asyncio.sleep(1)
        if not voice_client.is_playing():
            utils.delete_music()
            await voice_client.disconnect()
            break

@bot.tree.command(name="parar", description="Para a música atual")
async def parar(interaction: discord.Interaction):
    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message("Música parada", delete_after=3)
        utils.delete_music()
        await voice_client.disconnect()
    else:
        await interaction.response.send_message("Não há música tocando para parar", delete_after=3)
