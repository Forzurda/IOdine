import datetime
import json
import math
import os
import traceback
from pprint import pprint

import discord
from discord import app_commands, ui
from discord.ext import commands, tasks
from dotenv import load_dotenv
from pytz import timezone

import cogs.misc.ids as Ids

channel_ids = Ids.Channels()

async def load():
     for filename in os.listdir('./cogs'):
         if filename.endswith('.py'):
             await bot.load_extension(f'cogs.{filename[:-3]}')


load_dotenv()

'''
Create an .ENV File. I would store all sheet names, tokens, api keys and all that in there in case
this repo goes public
'''

token = os.getenv("TOKEN")

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.all(), 
            command_prefix='.',
            # Activity types are playing, gaming, listening, watching 
            activity=discord.Activity(type=discord.ActivityType.watching, name='In Development'))

    '''
    Use this versus load + asyncio. This is automatically ran when the bot comes online
    Be wary that iterating through the files in this fashion will ultimately make nested 
    directories more annoying to access. I.e. ./cogs/admin/administration.py
    '''    
    async def setup_hook(self):          
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')

    
    # Not really important, but console updating stating that the bot is live
    async def on_ready(self):
        pprint(f'✅ Running as {self.user}')

    # I don't think this ACTUALLY works. I think it needs to be put elsewhere, not sure
    async def on_error(self, event, interaction: discord.Interaction, *args, **kwargs):
        embed = discord.Embed(title=f':x: Event Error in IOd', colour=0xe74c3c)  # Red
        embed.add_field(name='Event', value=event)
        embed.description = 'py\n%s\n' % traceback.format_exc()
        
        # See the available PYTZ timezones and change this
        tz = timezone('Europe/Oslo')
        embed.timestamp = datetime.datetime.now(tz)
        await interaction.response.send_message(embed=embed)
    
    
# -----------------------------------------------------------------

client=commands.Bot(command_prefix=commands.when_mentioned_or("."))

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Option 1",emoji="👌",description="This is option 1!"),
            discord.SelectOption(label="Option 2",emoji="✨",description="This is option 2!"),
            discord.SelectOption(label="Option 3",emoji="🎭",description="This is option 3!")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)

    
# -----------------------------------------------------------------






bot = MyBot()
tree = bot.tree

@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    synced = await tree.sync(guild=discord.Object(id=1155194688375103592))
    await ctx.send(f"synced {len(synced)} Main commands")

bot.run(token)