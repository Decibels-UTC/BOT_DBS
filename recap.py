import discord
import json
import aiohttp
import time
import asyncio
import os
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import pymysql as MySQLdb

load_dotenv(find_dotenv())

def get_reminders():
    db = MySQLdb.connect(host=os.environ['DB_HOST'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'],
                         database=os.environ['DB_NAME'])
    cursor = db.cursor()
    query = "SELECT * FROM reminders WHERE date > NOW()";
    cursor.execute(query)
    tab = cursor.fetchall()
    db.close()
    return tab

def add_reminders(date, title, guild):
    db = MySQLdb.connect(host=os.environ['DB_HOST'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'],database=os.environ['DB_NAME'])
    cursor = db.cursor()

    now = datetime.now()
    # Format the date and time as a string in the desired format
    date_now = now.strftime('%Y-%m-%d %H:%M')

    parameters = (None, guild, title, date, date_now)
    query = "INSERT INTO reminders VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query, parameters)
    db.commit()
    db.close()

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents, description="BOT Discord pour l'association Décibels")
intents.members = True
intents.message_content = True

async def my_background_task():
    while True:
        now = datetime.now()
        now = str(now.strftime("%H:%M"))
        if now == "10:00":
            await all()
            await asyncio.sleep(60)
        await asyncio.sleep(45)



@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user} ! ")
    client.loop.create_task(my_background_task())


# Défitioon de l'object discord event avec ses méthodes pour intéragir avec :
# crédits à https://gist.github.com/adamsbytes/8445e2f9a97ae98052297a4415b5356f pour son code


@client.command()
async def get(ctx):


    t = DiscordEvents(os.environ['TOKEN'])
    lis = await t.list_guild_events(ctx.guild.id)
    channel = discord.utils.get(client.get_all_channels(), id=ctx.channel.id)
    embed = discord.Embed(title='Récapitulatif des events à venir', url="https://assos.utc.fr/assos/decibels", description="Petit rappel quotidien des events qui arrivent à grand pas : ",
                          color=discord.Color.yellow())
    embed.set_author(name='Décibels')
    embed.set_thumbnail(url="https://assos.utc.fr/images/assos/722b5410-3af5-11e9-bec2-a144d884ae44/1559292260.png")

    if(len(lis)==0):
        embed.add_field(name="Pas d'évent prévu pour le moment !", value='Oublies pas le ricard', inline=False)
    else:
        for item in lis:
            nom = item['name']
            desc = item['description'] + '\n@everyone'
            start = item['scheduled_start_time']

            start_time = time.strptime(start[:-6] + start[-6:].replace(":", ""), '%Y-%m-%dT%H:%M:%S%z')
            start_timestamp = time.mktime(start_time)
            start_utc = datetime.utcfromtimestamp(start_timestamp)
            date = start_utc.strftime('%d %m à %H:%M %Z')

            end = item['scheduled_end_time']
            place = item['entity_metadata']['location']

            text = desc+'\n'+f'Rendez vous à {place} le {date}.'
            embed.add_field(name=nom, value=text,inline=False)


    embed.set_footer(text="La décibise 🎛️")
    await channel.send(embed=embed)

async def all():
    channel = await client.fetch_channel(1084526010508259379)
    tab_all = []
    t = DiscordEvents(os.environ['TOKEN'])
    lis = await t.list_guild_events(1084493701943930981)
    tab = get_reminders()

    embed = discord.Embed(title="Récapitulatif de ce qu'il se passe dans DBS", url="https://assos.utc.fr/assos/decibels",
                          description="C'est pas toujours facile de penser à tout donc voici un rappel quotidien de ce qui arrive :",
                          color=discord.Color.yellow())
    embed.set_author(name='Décibels')
    embed.set_thumbnail(url="https://assos.utc.fr/images/assos/722b5410-3af5-11e9-bec2-a144d884ae44/1559292260.png")

    if (len(lis) == 0 and len(tab) == 0):

        embed.add_field(name="Rien de prévu pour l'instant", value="Tu peux aller te prendre un ricard", inline=False)

    else:
        for item in tab:
            name = item[2]
            date = item[3]
            date = date.strftime("%d %m à %H:%M")
            tab_all.append((name, date, '', ''))

        t = DiscordEvents(os.environ['TOKEN'])

        for item in lis:
            nom = item['name']
            desc = item['description']
            place = item['entity_metadata']['location']
            start = item['scheduled_start_time']

            start_time = time.strptime(start[:-6] + start[-6:].replace(":", ""), '%Y-%m-%dT%H:%M:%S%z')
            start_timestamp = time.mktime(start_time)
            start_utc = datetime.utcfromtimestamp(start_timestamp)
            date = start_utc.strftime('%d %m à %H:%M %Z')

            tab_all.append((nom, date, desc, place))

        for item in tab_all:
            text = item[2] + '\n' + f'Prévue le {item[1]}'
            if item[3] != '':
                text = text + f' à {item[3]}'
            embed.add_field(name=item[0], value=text, inline=False)

    tab_all = tab_all.sort(key=lambda x: x[1])
    print(tab_all)

    embed.set_footer(text="La décibise 🎛️")
    await channel.send(embed=embed)

@client.command()
async def remind(ctx, *args):
    if discord.utils.get(ctx.author.roles, name="Burö"):
        if(len(args)==0):
            await all()

        else:
                guild = ctx.guild.id
                try:
                    date = args[0].replace('T', ' ') + ':00'
                    text = ''
                    t = 0
                    for mot in args:
                        if t != 0:
                            text += mot + ' '
                        t += 1

                    add_reminders(date, text, guild)
                    await ctx.message.add_reaction('👍')
                except:
                    await ctx.channel.send(
                        f"Attention {ctx.author.mention}, le format pour ajouter des évennements au reminder est le suivant: mm-ddTHH:MM")
    else:
        await ctx.send("Tu n'as pas le rôle nécessaire pour exécuter cette commande.")

class DiscordEvents:
    '''Class to create and list Discord events utilizing their API'''

    def __init__(self, discord_token: str) -> None:
        self.base_api_url = 'https://discord.com/api/v9'
        self.auth_headers = {
            'Authorization': f'Bot {discord_token}',
            'User-Agent': 'DiscordBot (https://your.bot/url) Python/3.11 aiohttp/3.8.1',
            'Content-Type': 'application/json'
        }

    async def list_guild_events(self, guild_id: str) -> list:
        '''Returns a list of upcoming events for the supplied guild ID
        Format of return is a list of one dictionary per event containing information.'''
        event_retrieve_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.get(event_retrieve_url) as response:
                    response.raise_for_status()
                    assert response.status == 200
                    response_list = json.loads(await response.read())
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()
        return response_list

    async def create_guild_event(
            self,
            guild_id: str,
            event_name: str,
            event_description: str,
            event_start_time: str,
            event_end_time: str,
            event_metadata: dict,
            event_privacy_level=2,
            channel_id=None
    ) -> None:
        '''Creates a guild event using the supplied arguments
        The expected event_metadata format is event_metadata={'location': 'YOUR_LOCATION_NAME'}
        The required time format is %Y-%m-%dT%H:%M:%S'''
        event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        event_data = json.dumps({
            'name': event_name,
            'privacy_level': event_privacy_level,
            'scheduled_start_time': event_start_time,
            'scheduled_end_time': event_end_time,
            'description': event_description,
            'channel_id': channel_id,
            'entity_metadata': event_metadata,
            'entity_type': 3
        })

        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.post(event_create_url, data=event_data) as response:
                    response.raise_for_status()
                    assert response.status == 200
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()


client.run(os.environ['TOKEN'])
