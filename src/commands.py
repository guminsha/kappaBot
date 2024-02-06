import discord
from discord.ext import commands
from random import randint
import re
import openpyxl

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
    pattern = re.compile("([1-9][0-9]?|100)d([1-9][0-9]?|100)")
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
        await interaction.response.send_message(f"Invalido")

# Excel pokemon command
workbook_pokemons = openpyxl.load_workbook("src/assets/pokemons.xlsx")["Planilha1"]

@bot.tree.command(name="pokemon", description="Escolhe um pokemon aleatório para você")
async def hello(interaction: discord.Interaction):
    pokemon_choice = randint(2, 154)
    await interaction.response.send_message(f"Você é o: {workbook_pokemons[pokemon_choice][0].value}\nTipo: {workbook_pokemons[pokemon_choice][1].value}\n{workbook_pokemons[pokemon_choice][2].value}")

# @bot.command()
# async def oi(ctx):
#     await ctx.send(f"Oi, {ctx.message.author.mention}")
