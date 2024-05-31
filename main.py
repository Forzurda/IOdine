import datetime
import os
import traceback
from pprint import pprint
import discord
from discord import app_commands, ui
from discord.ext import commands, tasks
from dotenv import load_dotenv

import cogs.misc.ids as Ids

channel_ids = Ids.Channels()
intents = discord.Intents.all()
load_dotenv()
token = os.getenv("DC_BOT_TOKEN")

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.all(), 
            command_prefix='.',
            # Activity types are playing, gaming, listening, watching 
            activity=discord.Activity(type=discord.ActivityType.watching, name='In Development.'))

    # Use this versus load + asyncio. This is automatically ran when the bot comes online. 
    # Be wary that iterating through the files in this fashion will ultimately make nested directories more annoying to access. I.e. ./cogs/admin/administration.py
    
    async def setup_hook(self):          
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')

    
    # Not really important, but console updating stating that the bot is live
    async def on_ready(self):
        pprint(f'✅ Running as {self.user}')
    

bot = MyBot()
tree = bot.tree

# reloads all cogs, should not be a rate limit but consider doing specific cog reload in future
@bot.command(name="r")
@commands.is_owner()
async def re_load(ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.reload_extension(f'cogs.{filename[:-3]}')
                print(filename)
        await ctx.send(f"Reloaded {len(os.listdir('./cogs'))} cogs.")


@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    synced = await tree.sync(guild=discord.Object(id=1077859376414593124))
    await ctx.send(f"synced {len(synced)} Main commands.")

bot.run(token)