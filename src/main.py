import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from random import randint
import re

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="oi", description="Bot te diz oi de volta")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Oi, {interaction.user.mention}!") #ephemeral=True)

@bot.tree.command(name="diga", description="Bot diz algo específico")
async def hello(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.mention} disse: {thing_to_say}!")

@bot.tree.command(name="rd", description="Rola um dado de 20 lados")
async def rd(interaction: discord.Interaction, dice: str):
    pattern = re.compile("([1-9]|[0-9])d([1-9]|[0-9])")
    print(dice)
    print(pattern.search(dice))
    if(pattern.search(dice)):
        values_list = dice.split("d")
        dice_quantity = values_list[0]
        dice_type = values_list[1]
        list_dices = []

        for i in range(int(dice_quantity)):
            list_dices.append(randint(1,int(dice_type)))
        str_list_dices = [str(i) for i in list_dices]
        result_dices = ", ".join(str_list_dices)
        total_value_dices = sum(list_dices)

        await interaction.response.send_message(f"Você rolou {dice_quantity}d{dice_type}: {result_dices}\nTotal:({total_value_dices})")
    else:
        await interaction.response.send_message(f"Invalido")

@bot.command()
async def oi(ctx):
    await ctx.send(f"Oi, {ctx.message.author.mention}")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('!oi'):
#         await message.channel.send(f'Olá!{}')

bot.run(os.getenv('TOKEN'))