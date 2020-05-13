#!/usr/bin/env python3

from datetime import datetime
import discord
import os
import requests


DISCORD_CODE_MARKER = chr(96) * 3 # is backtick
DISCORD_MAX_MSG_LEN = 2000


def max_code_len(code_type: str) -> int:
    return DISCORD_MAX_MSG_LEN - (2 * len(DISCORD_CODE_MARKER)) - len(code_type) - 2


def rfind_space(s: str) -> int:
    for i, ch in enumerate(reversed(s)):
        if ch.isspace():
            return i

    return -1


def find_word_cut_index(s: str, max_len: int) -> int:
    if len(s) >= max_len:
        last_space = s.rfind(" ")
        if last_space > 0:
            return last_space

    return len(s)


def find_code_cut_index(s: str, max_len: int) -> int:
    front = s[:max_len]
    last_line = front.rfind("\n")

    if last_line > 0:
        return last_line
    else:
        return len(s)
        

def extract_file_extension(s: str) -> str:
    last_point = s.rfind(".")

    if last_point != -1:
        return s[last_point+1:]
    else:
        return ""


class LongMsgExpander(discord.Client):
    async def on_ready(self):
        print("<{}> ready".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S")))

    async def on_message(self, msg: discord.Message):
        if msg.content == "expand me daddy" and len(msg.attachments) == 1:
            first_attach  = msg.attachments[0]

            ext     = extract_file_extension(first_attach.filename)
            content = requests.get(first_attach.url).text


            is_code = False
            code_type = ""

            if ext == "txt":
                if content.startswith(DISCORD_CODE_MARKER) and content.endswith(DISCORD_CODE_MARKER):
                    is_code = True

                    first_line_end = content.find("\n")
                    if first_line_end != -1:
                        code_type = content[3:first_line_end]

                    content = content.splitlines()[1:-1].join("\n")
            else:
                is_code = True
                code_type = ext

            content = content.replace(DISCORD_CODE_MARKER, "\\" + DISCORD_CODE_MARKER)

            await msg.channel.send("**Author**: {}\n**File**: {}".format(msg.author.name, first_attach.filename))

            while len(content.strip()) > 0:
                if is_code:
                    MAX_CODE_LEN = max_code_len(code_type)

                    front = content[:MAX_CODE_LEN]
                    cut_idx = find_code_cut_index(content, MAX_CODE_LEN)
                    
                    await msg.channel.send("{marker}{code_type}\n{code}\n{marker}".format(
                        marker=DISCORD_CODE_MARKER,
                        code_type=code_type, 
                        code=front[:cut_idx]))

                    content = content[cut_idx:]
                else:
                    front = content[:DISCORD_MAX_MSG_LEN]
                    cut_idx = find_word_cut_index(front, DISCORD_MAX_MSG_LEN)

                    await msg.channel.send(front[:cut_idx])
                    content = content[cut_idx:]

            await msg.delete()


if __name__ == "__main__":
    tok = os.environ["LONG_MSG_EXPANDER_DISCORD_TOKEN"]
    
    client = LongMsgExpander()
    client.run(tok)
