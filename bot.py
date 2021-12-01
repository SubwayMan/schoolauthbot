import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import os
import time
import tempcURL
from adventdata import get_advent_data

load_dotenv()

ecv = commands.Bot(command_prefix="&")

        
@ecv.command(name="test")
async def sayhi(ctx):
    await ctx.channel.send("test")
    
@ecv.command(name="verify", pass_context=True)
async def verify(ctx, uid):
    student = ctx.message.author
    val = tempcURL.send_req(uid)
    if val == 1:
        await ctx.send("No user found.")
    elif val:
        role = get(student.guild.roles, name='Member')
        await student.add_roles(role)
        await ctx.send("Verified as " + val["DisplayName"])
    else:
        await ctx.send("Unknown error. Please try again later.")

@ecv.command(pass_context=True, name="aoclb")
async def advent_leaderboard(ctx, event="2021"):
    if not event.isnumeric() or not 2015<=int(event)<=2021:
        event = "2021"

    dat = get_advent_data(event)
    evn = "Advent of Code " + dat["event"]
    usr_data = dat["members"]
    url = "https://adventofcode.com/" + dat["event"]
    
    embd = discord.Embed(title=evn, url=url, description="Hamber Coding Club's leaderboard for Advent of Code {}".format(dat["event"]))
    whitespace = [12, 9, 9, 9]
    headers = ["Name", "Stars", "Local", "Global"]
    body = "```|" + "|".join(headers[k].ljust(whitespace[k]) for k in range(len(headers))) + "|"
    fields = ["name", "stars", "local_score", "global_score"]

    for k in sorted(usr_data, key=lambda a: usr_data[a]["local_score"],
            reverse=True):
        row = "\n"
        for elem, wh in zip(fields, whitespace):
            fieldval = str(usr_data[k][elem])[:wh-1].ljust(wh)
            row += "|" + fieldval
        row += "|"
        body += row
    
    body += "```"
    embd.add_field(name="Leaderboard", value=body)
    await ctx.send(embed=embd)








ecv.run(os.environ.get("bot-token"))
