import datetime
import json
import random
from itertools import cycle

import discord
import numpy as np
import pandas as pd
import requests
from discord.ext import commands, tasks
from dotenv import dotenv_values
from dotenv import load_dotenv

status = cycle(["killing myself", "not killing myself"])

poke_lis = pd.read_csv("pokemon.csv")
poke_arr = np.array(poke_lis["Name"].values)

bad = pd.read_csv("bad-words.csv")

bad_arr = np.array(bad["jigaboo"].values)

load_dotenv()
# getting dot env file

token = dotenv_values("token.env")
# returns key value pair which we convert into a dictionairy
token = dict(token)
guild_name = token["GUILD_TOKEN"]

# guild is essentially server name GUILD_TOKEN is server name

intent = discord.Intents.all()
intent.members = True
"""inent is required to access some features such as accessing names of people in the server"""
# client = discord.Client(intents=intent)

boti = commands.Bot(command_prefix="_", intents=intent)


# boti will not be initialized if intents parameter is not passed
# instead of discord.Intents.all() we can also use discord.Intents.default()
# then use intent.members = True to get member names


@boti.event
async def on_ready():
    # guild = discord.utils.get(client.guilds, name=guild_name)
    # await boti.change_presence(status=discord.Status.online , activity=discord.Game("killing myself"))
    change_status.start()
    print("bot is ready")

    """print(f"{client.user} has connected to discord!" + f"\n {guild.name} (id: {guild.id})")"""


"""printing names of server members based on the server name given in esv file (GUILD_TOKEN)"""


# print( f"{guild.member_count} are present in the server")
#  cnt= 0
#  for mem in guild.members:
#      print(f"- {mem.name}")
#      cnt+=1


@tasks.loop(seconds=5)
async def change_status():
    await boti.change_presence(activity=discord.Game(next(status)))


@boti.event
async def on_member_join(member):
    await member.create_dm()
    await member.send(f"{member.name} WELCOME to  {member.guild}")


@boti.command()
async def talk(ctx, *, message):
    if ("H" in message):
        await ctx.channel.send("chup kar chutad")


@boti.command(name="pokemon", help="returns name of random pokemon")
async def on_message(ctx):
    if ctx.author == boti.user:
        return

    response = random.choice(poke_arr)
    await ctx.send(response)


@boti.command(name="roll_dice", help="enter how many dice you want")
async def roll(ctx, n_die: int):
    dice = [str(random.choice(range(1, 6 + 1)))
            for _ in range(n_die)]

    await ctx.send(",".join(dice))


@boti.command(name="gaali", help="random english cusswor")
async def bad(ctx):
    await ctx.send(random.choice(bad_arr))


@boti.command(help="enter word or sentence and will get a gif")
async def gif(ctx, *, search):
    api_key = "AIzaSyAIRgBPCl4ekXyNw_pi_FdWXZPvUJ4tOl8"
    client_key = "mk223"
    lim = 8
    r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (
        search, api_key, client_key, lim))
    if r.status_code == 200:

        top8 = json.loads(r.content)

        await ctx.send(top8["results"][random.randint(0, 7)]["url"])

    else:
        await ctx.send("found nothing")


@boti.command(help="returns latency from bot to user which entered the command")
async def ping(ctx):
    await ctx.send(f"{round(boti.latency * 1000)}ms")


@boti.command(help="enter number of text messages you want to delete in sever channel")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@boti.command(help="can be used to kick a member")
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, why=None):
    await member.kick(reason=why)
    await ctx.send(f"kicked {member.mention}")


@boti.command(help="cna be used to ban a member")
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, why=None):
    await member.ban(reason=why)
    await ctx.send(f"banned {member.mention}")


@boti.command()
async def unban(ctx, *, member):
    obj = await commands.UserConverter().convert(ctx, member)
    if obj is None:
        id_ = await commands.IDConverter().convert(str(member))
        if id_ is not None:
            try:
                obj = await boti.fetch_user(int(id_.group(1)))
            except discord.NotFound:
                obj = None
        if obj is None:
            await ctx.send('User not found')
            return
    await ctx.guild.unban(obj)
    await ctx.send(f'Unbanned {obj}')


@boti.command(help='displays hour , minutes , seconds and microseconds  respectively in that order')
async def time(ctx):
    await ctx.send("TIMEZONE : IST \n")
    tm = str(datetime.datetime.time(datetime.datetime.now()))

    await ctx.send(tm[:2] + " hours " + tm[3:5] + " minutes " + tm[6:10] + " seconds ")


@boti.command(help ="annoy people you love the most")
async def spam(ctx, *, message=""):
    await ctx.send(message)

    await ctx.send(message)

    await ctx.send(message)

    await ctx.send(message)

@boti.command()
async def anger(ctx):
    api_key = "AIzaSyBE3EIUMTY6dgYF5_q8kpl7WSxW42g2484"
    client_key = "mk223"
    lim = 12
    search = "angry"
    r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (
        search, api_key, client_key, lim))
    if r.status_code == 200:

        top8 = json.loads(r.content)

        await ctx.send(top8["results"][random.randint(0, 10)]["url"])

    else:
        await ctx.send("found nothing")


boti.run(token["DISCORD_TOKEN"])
