import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime
import pymysql as MySQLdb
from enum import Enum
import asyncio

load_dotenv(find_dotenv())

intents = discord.Intents.default()
client = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="BOT Discord pour l'association Décibels",
)
intents.members = True
intents.message_content = True

field = Enum("field", ["id", "member_id", "original_username", "guild_id", "date"])
db = MySQLdb.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
)


async def restore_username_routine():
    # Define database fields
    global field
    global db
    last_count = 0
    while True:
        now = datetime.now()
        # Fetch all nickname change from database
        cursor = db.cursor()
        query = "SELECT COUNT(*) FROM user_rename"
        cursor.execute(query)
        tab = cursor.fetchall()

        if tab[0][0] != last_count:
            last_count = int(tab[0][0])
            query = "SELECT * FROM user_rename"
            cursor.execute(query)
            tab = cursor.fetchall()
            for row in tab:
                # Parse database datetime into python datetime
                date = datetime.strptime(row[field.date.value], "%Y-%m-%d %H:%M:%S.%f")
                # If 24h has passed since the nickname change
                if (now - date).days >= 1:
                    # Restore the nickname
                    guild = client.get_guild(int(row[field.guild_id.value]))
                    member = guild.get_member(int(row[field.member_id.value]))
                    await member.edit(nick=row[field.original_username.value])
                    # Delete the nickname change from database
                    query = f"DELETE FROM user_rename WHERE id = {row[field.id.value]}"
                    cursor.execute(query)
                    db.commit()
        asyncio.sleep(300)


@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user} ! ")


@client.event
async def on_message(message):
    global field
    global db

    if message.author == client.user:
        return

    words = message.content.lower().split()  # On prend les 10 premiers mots
    phrase = " ".join(words)  # On transforme les mots en une phrase

    if "je suis" in phrase:
        if message.author.id != 463652129878573056:  # if pas Cesar
            index = words.index("je") + 1
            try:
                if words[index] == "suis":
                    # Récupérer les mot suivant et l'envoyer en réponse
                    t = " ".join(words[index + 1 :])

                    member = message.author
                    await member.edit(nick=t)

                    response = f"Le pseudo de {member.mention} vient dêtre modifié !"
                    await message.channel.send(response)
                    # Get the current datetime
                    now = datetime.now()
                    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    # Add nickname change to database
                    cursor = db.cursor()
                    query = f"INSERT INTO user_rename (member_id, original_username, guild_id, date) VALUES ({None}, {member.id}, {member.name}, {message.guild.id}, {formatted_date})"
                    cursor.execute(query)
                    db.commit()
            except:
                try:
                    t = " ".join(words[index + 1 : index + 2])
                    member = message.author
                    await member.edit(nick=t)

                    response = (
                        f"Le pseudo de {member.mention} vient dêtre modifié !\cheh"
                    )
                    await message.channel.send(response)
                    # Get the current datetime
                    now = datetime.now()
                    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    # Add nickname change to database
                    cursor = db.cursor()
                    query = f"INSERT INTO user_rename (member_id, original_username, guild_id, date) VALUES ({None}, {member.id}, {member.name}, {message.guild.id}, {formatted_date})"
                    cursor.execute(query)
                    db.commit()

                except:
                    await message.channel.send(f"Bien esquivé  {member.mention}")
        else:
            await message.channel.send(
                f"Il y en a qui ont des passe droits ! {member.mention}"
            )


# Remplacez le TOKEN avec votre propre token de bot Discord
client.run(os.environ["TOKEN"])
