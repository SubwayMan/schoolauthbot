#!/usr/bin/env python3
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import os
import time
import tempcURL
import challengers
import random
from adventdata import get_advent_data

load_dotenv()

ecv = commands.Bot(command_prefix="&")
challengers_questions = challengers.load_questions()


@ecv.command(name="test")
async def sayhi(ctx):
    await ctx.channel.send("test")


@ecv.command(pass_context=True, name="verify")
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
    if not event.isnumeric() or not 2015 <= int(event) <= 2021:
        event = "2021"

    dat = get_advent_data(event)
    evn = "Advent of Code " + dat["event"]
    usr_data = dat["members"]
    url = "https://adventofcode.com/" + dat["event"]

    embd = discord.Embed(title=evn, url=url, description="Hamber Coding Club's leaderboard for Advent of Code {},\n displaying top 20 participants.".format(dat["event"]))
    whitespace = [12, 9, 9, 9]
    headers = ["Name", "Stars", "Local", "Global"]
    body = "```|" + "|".join(headers[k].ljust(whitespace[k]) for k in range(len(headers))) + "|"
    fields = ["name", "stars", "local_score", "global_score"]

    for k in sorted(usr_data, key=lambda a: (usr_data[a]["local_score"], usr_data[a]["stars"], usr_data[a]["name"]), reverse=True)[:20]:
        row = "\n"
        for elem, wh in zip(fields, whitespace):
            fieldval = str(usr_data[k][elem])[:wh-1].ljust(wh)
            row += "|" + fieldval
        row += "|"
        body += row

    embd.add_field(name="Leaderboard", value=body[:1021]+"```")
    await ctx.reply(embed=embd)


@ecv.command(pass_context=True, name="math")
async def create_problem(ctx):
    problem_data = random.choice(challengers_questions)
    problem = challengers.Problem(problem_data)
    embed, img = problem.get_embed(0xebd300)
    await ctx.reply(embed=embed, file=img)


@ecv.command(pass_context=True, name="answer")
async def submit_answer(ctx, qid, *, answer):

    if not qid.isnumeric():
        await ctx.reply("Invalid problem ID.")
        return

    qid = int(qid)
    status, result = challengers.Problem.submit_answer(qid, answer)
    if status != 0:
        await ctx.reply("Invalid problem ID.")
    else:
        problem = challengers.Problem.loaded_problems[qid]
        if result:
            embed, img = problem.get_embed(0x2bff00)
            embed.add_field(name="Answer", value="`" + problem.answer + "`")
            await ctx.reply("Correct!", embed=embed, file=img)

            challengers.Problem.unload_question(qid)
        else:
            embed, img = problem.get_embed(0xbd1c37)
            await ctx.reply("Incorrect!", embed=embed, file=img)


@ecv.command(pass_context=True, name="active")
async def active_problems(ctx):
    problem_ids = challengers.Problem.loaded_problems.keys()
    contents = "\n".join(map(str, problem_ids))[:1021]
    if contents == "":
        contents = "Nothing here..."

    body = "```\n{}\n```".format(contents)
    description = """Here is a list of all currently open problem IDs. 
    Use &view to see the problem statement. Note that a problem is closed
    after it has been answered correctly."""
    title = "Open Problems"
    embed = discord.Embed(title=title, description=description)
    embed.add_field(name="ID", value=body)
    embed.color = 0x9ec90e
    await ctx.reply(embed=embed)


@ecv.command(pass_context=True, name="view")
async def view_problem(ctx, qid):
    if not qid.isnumeric():
        await ctx.reply("Invalid problem ID.")
        return
    qid = int(qid)
    if qid in challengers.Problem.loaded_problems:
        problem = challengers.Problem.loaded_problems[qid]
        embed, img = problem.get_embed(0xebd300)
        await ctx.reply(embed=embed, file=img)
    else:
        await ctx.reply("Invalid problem ID.")


ecv.run(os.environ.get("bot-token"))
