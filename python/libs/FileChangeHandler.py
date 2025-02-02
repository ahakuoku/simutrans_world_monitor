import enum
from typing import Dict
import config
import os
import hashlib
import asyncio
import json
import discord
from watchdog.events import FileSystemEventHandler
from libs.vars import *

FILE_OUT = config.DIRECTORY + '/file_io/out.txt'
FILE_EMBED = config.DIRECTORY + '/file_io/out_embed.json'

DISCORD_MAX_TEXT_LENGTH = 1950

class FileChangeHandler(FileSystemEventHandler):
    def discord_text_escape(self, str: str) -> str:
        return str.translate(str.maketrans({'*': '\\*', '_': '\\_', '~': '\\~', '|': '\\|', '`': '\\`', ':': '\\:'}))
    
    def remove_waiting_message(self, ch):
        if get_waiting_message()!=None:
            coro = ch.delete_messages([get_waiting_message()])
            asyncio.run_coroutine_threadsafe(coro, client.loop)
            set_waiting_message(None)
    
    def is_same_message(self, str):
        hash = hashlib.md5(str.encode()).hexdigest()
        if hash==get_prev_out_hash():
            return True
        else:
            set_prev_out_hash(hash)
            return False
    
    def plain_text_out(self):
        with open(FILE_OUT, encoding='utf-8') as f:
            s = self.discord_text_escape(f.read())
            if s is None or s=='empty' or self.is_same_message(s):
                return
            ch = client.get_channel(config.CHANNEL_ID)
            self.remove_waiting_message(ch)
            if s <= DISCORD_MAX_TEXT_LENGTH :
                coro = ch.send(s)
                asyncio.run_coroutine_threadsafe(coro, client.loop)
            else:
                s_sprited: list = s.split('\n')
                message_list: list = []
                message: str = ""
                for line in s_sprited:
                    if len(message) + len(line) >= DISCORD_MAX_TEXT_LENGTH :
                        message_list += [message]
                        message = ""
                    message += line + '\n'
                else:
                    message_list += [message]
                for i, message in enumerate(message_list):
                    coro = ch.send(f'(Part {i + 1}/{len(message_list)})\n``{message}``')
                    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass
    
    def embed_out(self):
        with open(FILE_EMBED, encoding='utf-8') as f:
            s = f.read()
            if len(s)==0 or self.is_same_message(s):
                return
            ch = client.get_channel(config.CHANNEL_ID)
            self.remove_waiting_message(ch)
            jo = json.JSONDecoder().raw_decode(s)[0]
            if jo["description"] is None:
                jo["description"] = ""
            if len(jo["description"]) <= DISCORD_MAX_TEXT_LENGTH:
                embed = discord.Embed(title=jo["title"], description=self.discord_text_escape(jo["description"]), color=jo["color"])
                if jo["fields"]:
                    for f in jo["fields"]:
                        embed.add_field(name=f["name"], value=f["value"], inline=True)
                if jo["footer"]:
                    embed.set_footer(text=jo["footer"])
                coro = ch.send(embed=embed)
                asyncio.run_coroutine_threadsafe(coro, client.loop)
            else:
                desc_sprited: list = self.discord_text_escape(jo["description"]).split('\n')
                message_list: list = []
                message: str = ""
                for line in desc_sprited:
                    if len(message) + len(line) >= DISCORD_MAX_TEXT_LENGTH :
                        message_list += [message]
                        message = ""
                    message += line + '\n'
                else:
                    message_list += [message]
                for i, message in enumerate(message_list):
                    embed = discord.Embed(title=jo["title"] + f" (Part {i + 1}/{len(message_list)})", description=message, color=jo["color"])
                    if jo["fields"]:
                        for f in jo["fields"]:
                            embed.add_field(name=f["name"], value=f["value"], inline=True)
                    if jo["footer"]:
                        embed.set_footer(text=jo["footer"])
                    coro = ch.send(embed=embed)
                    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass
    
    # ファイル変更時のイベント
    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        if filename=="out.txt" :
            self.plain_text_out()
        elif filename=="out_embed.json" :
            self.embed_out()
            pass
