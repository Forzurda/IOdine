import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc.roles import Roles
from cogs.misc import utils


role_ids = Roles()

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('General cog loaded')
 

    @app_commands.command(name="bot_ping", description="see how shit internet I have xddds")
    async def ping(self, ctx):
        await ctx.response.send_message(f"{round(self.bot.latency *1000)}ms.")
    
    @app_commands.command(name='clear', description='clear [number] of messages')
    @commands.is_owner()
    async def clear(self, msg: discord.Interaction, number: int):
        await msg.response.send_message(embed=utils.embed_success(f'Deleted {number} message(s)'), ephemeral=True)
        await msg.channel.purge(limit=number)

    @commands.command()
    async def sync_general(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1155194688375103592))
            await ctx.send(f"synced {len(synced)} General commands")
        except discord.HTTPException as er:
            await ctx.send(er)

async def setup(bot):
    await bot.add_cog(General(bot), guilds=[discord.Object(id=1155194688375103592)])