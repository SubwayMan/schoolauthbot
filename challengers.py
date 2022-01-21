import re
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

        self.answer = self.answer[0]
        self.hash = random.randrange(int(1E7), int(1E8))
        Problem.loaded_problems[self.hash] = self

    def get_embed(self) -> discord.Embed:
        """Sends a discord-sendable embed representation of problem."""
        embed = discord.Embed(title="Math Challengers Practice", description="Question ID: {}".format(self.hash))
        embed.add_field(name=self.description, value=self.body)
        return embed

    def check_answer(self, answer) -> bool:
        """Verifies answer."""
        if answer.strip().replace() == self.answer:
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


def load_questions():
    with open("questions.txt", "r") as all_data:
        questions = all_data.read().split("~")
    return questions
