import discord
import json
from dotenv import load_dotenv
from dotenv import dotenv_values
import pandas as pd
import numpy as np
import random
import requests
import datetime


from discord.ext import commands,tasks
from itertools import cycle

status = cycle(["killing myself" , "not killing myself"])



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

intent = discord.Intents.all()

intent.members = True

client = discord.Client(intents=intent)

boti = commands.Bot(command_prefix="_", intents=intent)


@boti.event
async def on_ready():
   # guild = discord.utils.get(client.guilds, name=guild_name)
    #await boti.change_presence(status=discord.Status.online , activity=discord.Game("killing myself"))
    change_status.start()
    print("bot is ready")


    """print(f"{client.user} has connected to discord!" + f"\n {guild.name} (id: {guild.id})")"""


"""printing names of server members based on the server name given in esv file (GUILD_TOKEN)"""


# print( f"{guild.member_count} are present in the server")
#  cnt= 0
#  for mem in guild.members:
#      print(f"- {mem.name}")
#      cnt+=1
@tasks.loop(seconds=10)
async def change_status():
    await boti.change_presence(activity=discord.Game(next(status)))

@boti.event
async def on_member_join(member):
    await member.create_dm()
    await member.send(f"{member.name} WELCOME")


# @boti.event
# async def on_message(message):
#
#     if("joke" in message.content):
#         await message.channel.send("chup kar chutad")


@boti.command(name="pokemon", help="returns name of random pokemon")
async def on_message(ctx):
    if ctx.author == client.user:
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
async def gif(ctx, *,search):
    api_key = "AIzaSyBE3EIUMTY6dgYF5_q8kpl7WSxW42g2484"
    client_key = "mk223"
    lim = 8
    r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (
    search, api_key, client_key, lim))
    if r.status_code == 200:

        top8 = json.loads(r.content)

        await ctx.send(top8["results"][random.randint(0,7)]["url"])

    else:
        await ctx.send("found nothing")




@boti.command(help= "returns latency from bot to user which entered the command")
async def ping(ctx):
    await ctx.send(f"{round(boti.latency * 1000)}ms")


@boti.command(help="enter number of text messages you want to delete in sever channel")
@commands.has_permissions(administrator=True)
async def clear(ctx,amount : int):
    await ctx.channel.purge(limit=amount)


@boti.command(help="can be used to kick a member")
@commands.has_permissions(administrator=True)
async def kick(ctx , member :discord.Member, *, why=None):
    await member.kick(reason=why)
    await ctx.send(f"kicked {member.mention}")


@boti.command(help="cna be used to ban a member")
@commands.has_permissions(administrator=True)
async def ban(ctx , member : discord.Member , *,why=None):
    await member.ban(reason=why)
    await ctx.send(f"banned {member.mention}")


@boti.command()
async def unban(ctx, *, member):
    obj = await commands.UserConverter().convert(ctx, member)
    if obj is None:
        id_ = await commands.IDConverter().convert(str(member))
        if id_ is not None:
            try:
                obj = await client.fetch_user(int(id_.group(1)))
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

    await ctx.send(tm[:2]+" hours " + tm[3:5] + " minutes " + tm[6:10] + " seconds ")




boti.run(token["DISCORD_TOKEN"])



