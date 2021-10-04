import discord
from dotenv import load_dotenv
import os
import time
import tempcURL

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        a, *b  = message.content.split()
        if len(b) == 1 and a == "$verify":
            response = tempcURL.send_req(b[0])
            if response == 1:
                await message.channel.send("No user found!")
            else:
                await message.channel.send(response["DisplayName"])

    async def on_message_delete(self, message):
        print(f"Caught in 4k: {message.author} said \"{message.content}\"")

client = MyClient()
client.run(os.environ.get("bot-token"))
