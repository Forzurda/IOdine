import discord
import math
from typing import Optional, List
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from discord.utils import *
from cogs.misc.roles import Roles
from cogs.misc import utils


class Calendar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('Calendar cog loaded')

# --------------------------------- /add event
    @app_commands.command(name="add_event", description="adds an event to the calendar")
    async def addevent(self, ctx):
        await ctx.send(f"Add Event command worked")

    


# --------------------------------- /.sync_general  (sync commands you dummy)
    
    @commands.command()
    async def sync_calendar(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync()
            await ctx.send(f"synced {len(synced)} Calendar commands")
        except discord.HTTPException as er:
            await ctx.send(er)

async def setup(bot):
    await bot.add_cog(Calendar(bot))
