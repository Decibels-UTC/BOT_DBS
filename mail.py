import asyncio
import imaplib
import email
import os
import time
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

intents = discord.Intents.default()
client = commands.Bot(command_prefix='.', intents=intents, description="Bot qui redirige les mails ver sun serveur discord.")
intents.members = True
intents.message_content = True


async def my_background_task():
    while True:
        try:
            await send_report(1106272550432030751)
        except:
            pass
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user} ! ")
    client.loop.create_task(my_background_task())


async def send_report(chann_id):
    try:
        channel = client.get_channel(chann_id)
        data = check_mail()
        for i in range(data[0]):
            subject = data[1][i]
            body = data[2][i]
            sender = data[3][i]

            embed = discord.Embed(title=subject, url="https://assos.utc.fr/mail",
                                  description=body,
                                  color=discord.Color.red())
            embed.set_author(name=sender)
            embed.set_thumbnail(url="https://assos.utc.fr/images/assos/722b5410-3af5-11e9-bec2-a144d884ae44/1559292260.png")
            embed.set_footer(text="La décibise 🎛️")

            await channel.send(embed=embed)
    except Exception as e:
        print(f"Error sending report: {e}")


def check_mail():

    imap_host = 'imap.gmail.com'
    imap_user = os.environ['MAIL']
    imap_password = os.environ['MAIL_PASSWORD']


    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(imap_user, imap_password)
    mail.select('inbox')


    status, messages = mail.search(None, 'UNSEEN')
    message_ids = messages[0].split()

    subjects = []
    bodies = []
    senders = []

    for id in message_ids:
        status, data = mail.fetch(id, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        subjects.append(msg['Subject'])
        senders.append(msg['From'])
        if msg.is_multipart():

            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':

                    bodies.append(part.get_payload(decode=True).decode('utf-8'))
        else:

            bodies.append(msg.get_payload(decode=True).decode('utf-8'))

        # Marquer l'email comme lu
        mail.store(id, '+FLAGS', '\\Seen')

    # Fermer la connexion
    mail.close()
    mail.logout()

    # Retourner les sujets, les corps et les expéditeurs des emails non lus
    return len(subjects),subjects, bodies, senders




client.run(os.environ['TOKEN'])
