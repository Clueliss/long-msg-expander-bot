#!/usr/bin/env python3

import discord
import os
import requests


def find_cut_index(s: str) -> int:
    if len(s) >= 2000:
        last_space = s.rfind(" ")
        if last_space > 0:
            return last_space

    return len(s)


class LongMsgExpander(discord.Client):
    async def on_ready(self):
        print("ready")

    async def on_message(self, msg: discord.Message):
        if msg.content == "" and len(msg.attachments) == 1:
            first_attach  = msg.attachments[0]

            if first_attach.filename == "message.txt":
                content = requests.get(first_attach.url).text

                await msg.channel.send("**Author: {}**".format(msg.author.name))

                while len(content) > 0:
                    front: str = content[:2000]
                    cut_idx = find_cut_index(front)

                    await msg.channel.send(front[:cut_idx])

                    content = content[cut_idx:]
            
            await msg.delete()


if __name__ == "__main__":
    tok = os.environ["LONG_MSG_EXPANDER_DISCORD_TOKEN"]
    
    client = LongMsgExpander()
    client.run(tok)
