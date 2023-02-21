#!/bin/python3

#1. Command to add a link --DONE--
#2. Bot pings user when link is in stock and removes link
#3. Command to see all links
#4. Command to see all links will also list item's title
#5. Notifier will ping all users who added same link
#6. >help page
#7. Add FileIO for persistence

import discord
from discord.ext import tasks

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.counter = 0
        self.URLS = []

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

        if message.content.split(' ')[0] == '>add':
            if len(message.content.split(' ')) == 1:
                await message.channel.send(f'Please enter a URL. Usage: `>add URL`')
            elif len(message.content.split(' ')) >= 3:
                await message.channel.send(f'Too many arguments. Usage: `>add URL`')
            elif 'https://www.bestbuy.com/site/' not in message.content.split(' ')[1]:
                await message.channel.send(f'Please enter a valid BestBuy URL. Usage: `>add URL`')
            else:
                await message.channel.send(f'Added {message.content.split(" ")[1]} to watch list')
                self.URLS.append([message.content.split(" ")[1], message.author.id])

    @tasks.loop(seconds=60)
    async def item_watcher(self):
        channel = self.get_channel(00000000) # channel ID (no quotes)
        watch_list = ''
        for url in self.URLS:
            watch_list += '' + str(url[0]) + '\n'
        await channel.send(f'Here is a list of all current URLs that are being watched :3\n' + watch_list)
            

    @item_watcher.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = MyClient(intents=intents)
client.run('token') # bot token (in quotes)