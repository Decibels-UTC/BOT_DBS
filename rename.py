# coding=utf-8

import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime
import pymysql as MySQLdb
from enum import Enum
import asyncio
import random as rd

load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="BOT Discord pour l'association Décibels",
)
intents.members = True
intents.message_content = True

field = Enum(
    "field", ["id", "member_id", "original_username", "guild_id", "date"], start=0
)
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
    last_count = -1
    while True:
        now = datetime.now()
        # Fetch all nickname change from database
        cursor = db.cursor()
        query = "SELECT COUNT(*) FROM user_rename"
        cursor.execute(query)
        tab_2 = cursor.fetchall()

        if tab_2[0][0] != last_count:
            last_count = int(tab_2[0][0])
            query = "SELECT * FROM user_rename"
            cursor.execute(query)
            tab = cursor.fetchall()
        for row in tab:
            # Parse database datetime into python datetime
            date = row[field.date.value]
            # If 24h has passed since the nickname change
            if (now - date).days >= 1:
                # Restore the nickname
                guild = client.get_guild(int(row[field.guild_id.value]))
                await guild.fetch_member(int(row[field.member_id.value]))
                member = guild.get_member(int(row[field.member_id.value]))
                await member.edit(nick=row[field.original_username.value])
                # Delete the nickname change from database
                query = f"DELETE FROM user_rename WHERE id = {row[field.id.value]}"
                cursor.execute(query)
                db.commit()
        await asyncio.sleep(300)





@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user} ! ")
    client.loop.create_task(restore_username_routine())




def get_excluded():
    global db
    cursor = db.cursor()
    query = "SELECT member_id FROM excluded"
    cursor.execute(query)
    tab = cursor.fetchall()
    tab = [int(i[0]) for i in tab]
    return tab


@client.event
async def on_message(message):
    global field
    global db
    cursor = db.cursor()
    member = message.author

    if member == client.user:
        return

    words = message.content.lower().split()  # On prend les 10 premiers mots
    phrase = " ".join(words)  # On transforme les mots en une phrase



    if "je suis" in phrase:
        if rd.randint(0, 2) < 1:

            if message.author.id not in get_excluded():  # if pas Cesar
                index = words.index("je") + 1
                try:
                    if words[index] == "suis":
                        # Récupérer les mot suivant et l'envoyer en réponse
                        t = " ".join(words[index + 1 :])

                        former_name = member.display_name
                        await member.edit(nick=t)
                        response = (
                            f"Le pseudo de {member.mention} vient dêtre modifié !"
                        )
                        await message.channel.send(response)
                        # Get the current datetime
                        now = datetime.now()
                        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                        # If user already in database

                        query = (
                            f"SELECT * FROM user_rename WHERE member_id = {member.id}"
                        )
                        cursor.execute(query)
                        tab = cursor.fetchall()
                        if len(tab) > 0:
                            # Update nickname change in database
                            query = f"UPDATE user_rename SET date = '{formatted_date}' WHERE member_id = {member.id}"
                            cursor.execute(query)
                            db.commit()
                        else:
                            # Add nickname change to database
                            parameters = (
                                None,
                                member.id,
                                former_name,
                                message.guild.id,
                                formatted_date,
                            )
                            query = "INSERT INTO user_rename VALUES(%s, %s, %s, %s, %s)"
                            cursor.execute(query, parameters)
                            db.commit()
                except:
                    try:
                        t = " ".join(words[index + 1 : index + 2])
                        former_name = member.display_name
                        await member.edit(nick=t)

                        response = (
                            f"Le pseudo de {member.mention} vient dêtre modifié !\cheh"
                        )
                        await message.channel.send(response)
                        # Get the current datetime
                        now = datetime.now()
                        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                        # If user already in database
                        query = (
                            f"SELECT * FROM user_rename WHERE member_id = {member.id}"
                        )
                        cursor.execute(query)
                        tab = cursor.fetchall()
                        if len(tab) > 0:
                            # Update nickname change in database
                            query = f"UPDATE user_rename SET date = '{formatted_date}' WHERE member_id = {member.id}"
                            cursor.execute(query)
                            db.commit()
                        else:
                            # Add nickname change to database
                            parameters = (
                                None,
                                member.id,
                                former_name,
                                message.guild.id,
                                formatted_date,
                            )
                            query = "INSERT INTO user_rename VALUES(%s, %s, %s, %s, %s)"
                            cursor.execute(query, parameters)
                            db.commit()

                    except:
                        await message.channel.send(f"Bien esquivé  {member.mention}")
            else:
                await message.channel.send(
                    f"Il y en a qui ont des passe droits ! {member.mention}"
                )


# Remplacez le TOKEN avec votre propre token de bot Discord
client.run(os.environ["TOKEN"])
