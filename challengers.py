import re
import discord


class problem():
    """
    Load a math challengers problem from raw data to parseable input.
    Formatting specification:
    [question statement]
    [newline]
    [tags]
    Current tags:
        A: Answer - a required tag that specifies the answer to the problem.
        P: Name of a diagram to attach.
        D: Problem type: examples include "Blitz", "Bulls-eye", etc.
    """

    def __init__(self, txt):
        self.body = txt.split("\n")[0]
        self.answer = re.findall(r"A\[(.+)\]", txt)
        self.diagram = re.findall(r"P\[(.+)\]", txt)
        self.description = re.findall(r"D\[(.+)\]", txt)

    def get_embed(self):
        embed = discord.Embed(title="Math Challengers Practice")

