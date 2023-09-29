import discord
from discord.ext import commands
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

intents = discord.Intents.all()
intents.guilds = True
intents.messages = True
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():

    print(f"connecté en tant que {client.user.name}")


@client.command()
async def addrole(ctx, *args):
    guild = ctx.guild
    roles = ctx.author.roles
    verif = False
    for role in roles:
        if role.name =="admin":
            verif = True
    if verif:
        role = discord.utils.get(guild.roles, name='admin') # bien rentrer le nom du role comme sur le serveur
        for item in args:
            item = item.replace("<", "")
            item = item.replace(">", "")
            item = item.replace("@", "")
            if '&' in item:
                item = item.replace('&','')
            item = int(item)

            member = guild.get_member(item)
            member_verif = True
            member_roles = member.roles
            for role in member_roles:
                if role.name == "admin":
                    member_verif = False
            if member_verif:
                await member.add_roles(role)
                await ctx.send(f"Le role admin a bien été ajouté à {member.mention}.")
            else:
                await ctx.send(f"{member.mention} a déjà le rôle admin.")

    else:
        await ctx.send("Vous n'avez pas le rôle requis pour effectuer cette action.")



@client.command()
async def removerole(ctx):
    guild = ctx.guild
    roles = ctx.author.roles
    verif = False
    for role in roles:
        if role.name =="admin":
            verif = True
    if verif:
        role = discord.utils.get(guild.roles, name='admin') # bien rentrer le nom du role comme sur le serveur
        await ctx.author.remove_roles(role)
        await ctx.send(f"Le role admin vous a bien été retiré.")
    else:
        await ctx.send("Vous n'avez pas le rôle requis pour effectuer cette action.")


client.run(os.environ["TOKEN"])
