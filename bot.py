import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import os
import time
import tempcURL

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

ecv.run(os.environ.get("bot-token"))
