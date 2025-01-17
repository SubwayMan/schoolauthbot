import re
import os
import discord
import random


class Problem():
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

    loaded_problems = dict()

    def __init__(self, txt):
        self.body = txt.split("\n\n")[0]
        self.answer = re.findall(r"A\[(.+)\]", txt)
        self.diagram = re.findall(r"P\[(.+)\]", txt)
        self.description = re.findall(r"D\[(.+)\]", txt)

        if self.description == []:
            self.description = None
        else:
            self.description = self.description[0]

        self.diagram = re.findall(r"P\[(.+)\]", txt)
        if self.diagram:
            self.diagram = self.diagram[0]

        self.answer = self.answer[0]
        self.hash = random.randrange(int(1E3), int(1E4))
        while self.hash in Problem.loaded_problems:
            self.hash = random.randrange(int(1E5), int(1E6))

        Problem.loaded_problems[self.hash] = self

    def get_embed(self, color=None) -> discord.Embed:
        """Sends a discord-sendable embed representation of problem."""
        embed = discord.Embed(title="Math Challengers Practice", description="Question ID: {}".format(self.hash), color=color)
        img = None
        if self.diagram:
            img = discord.File(os.path.join("challengers-diagrams", self.diagram))
            embed.set_image(url="attachment://" + self.diagram)
        embed.add_field(name=self.description, value=self.body)
        return (embed, img)

    def check_answer(self, answer) -> bool:
        """Verifies answer."""
        if answer.strip() == self.answer:
            return True
        return False

    def submit_answer(problem_id, answer) -> (int, bool):
        """Class-specific function that checks if a specific problem id exists
        and if so sends the provided answer to the problem's check_answer function."""

        if problem_id in Problem.loaded_problems:
            problem = Problem.loaded_problems[problem_id]
            if problem.check_answer(answer):
                return (0, True)
            return (0, False)
        return (-1, False)

    def unload_question(problem_id):
        """Removes a problem id from loaded problems."""

        if problem_id in Problem.loaded_problems:
            Problem.loaded_problems.pop(problem_id)


def load_questions():
    with open("questions.txt", "r", encoding="utf-8") as all_data:
        questions = all_data.read().split("~")
    return questions
