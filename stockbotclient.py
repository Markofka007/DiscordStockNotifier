#!/bin/python3

#1. Command to add a link --DONE--
#2. Bot pings user when link is in stock and removes link --Done--
#3. Command to see all links --DONE--
#5. Notifier will ping all users who added same link
#6. >help page
#7. Add FileIO for persistence

import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup


def get_url_content(target_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36'}
    response = requests.get(target_url, headers=headers)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.counter = 0
        self.URLS = [] # [['https://www.bestbuy.com/site/apple-airpods-pro-2nd-generation-white/4900964.p?skuId=4900964', 204790558395203585]]
        self.announcement_channel = self.get_channel(int())

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.item_watcher.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)

    async def on_message(self, message):
        print(f"{message.author} says {message.content}")
        #print(message)
        if message.author == self.user:
            return

        if message.content == '>ping':
            await message.channel.send(f'<@{message.author.id}>')

        if message.content.split(' ')[0] == '>addlink':
            arg1 = message.content.split(' ')[1]
            if len(message.content.split(' ')) == 1:
                await message.channel.send(f'Please enter a URL. Usage: `>addlink URL`')
            elif len(message.content.split(' ')) >= 3:
                await message.channel.send(f'Too many arguments. Usage: `>addlink URL`')
            elif 'https://www.bestbuy.com/site/' not in arg1:
                await message.channel.send(f'Please enter a valid BestBuy URL. Usage: `>addlink URL`')
            else:
                await message.channel.send(f'Added `{get_url_content(arg1).find("title").text}` to watch list')
                self.URLS.append([arg1, message.author.id])

        if message.content == '>showlinks':
            watch_list = ''
            for url in self.URLS:
                watch_list += '' + str(url[0]) + '\n'
            await message.channel.send(f'Here is a list of all current URLs that are being watched:\n' + watch_list)

        if message.content.split(' ')[0] == '>setchannel': # and message.author.permissions.administrator
            arg1 = message.content.split(' ')[1]
            arg2 = message.content.split(' ')[2]
            if arg1 == 'announcements':
                self.announcement_channel = self.get_channel(int(arg2))
                await message.channel.send(f'Changed announcement channel to <#{int(arg2)}>')

    @tasks.loop(seconds=1)
    async def item_watcher(self):
        #await self.announcement_channel.send("test")
        for url in self.URLS:
            print(f"Checking URL {url[0]}")
            source_code = str(get_url_content(url[0]))
            #print(str(get_url_content(url[0])))
            with open("output.txt", "w") as file:
                file.write(source_code)
            if '\\"availability\\":1' in source_code:
                print('URL in stock')
                await self.announcement_channel.send(f'<@{url[1]}> {url[0]} IS IN STOCK!!! :D')
                self.URLS.remove(url)
            else:
                print("Nope")

    @item_watcher.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in
        self.announcement_channel = self.get_channel(00000000000) # Channel ID


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = MyClient(intents=intents)
client.run('token') # Bot Token (in quotes)