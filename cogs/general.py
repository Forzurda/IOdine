import discord
from typing import Optional, List
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

# --------------------------------- /ping chilling
    @app_commands.command(name="bot_ping", description="see how shit internet I have xddds")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{round(self.bot.latency * 1000)}ms.")
    
    
# --------------------------------- /nuke 1hor
    @app_commands.command(name='clear', description='clear [number] of messages')
    @commands.is_owner()
    async def clear(self, interaction: discord.Interaction, number: int):
        await interaction.response.send_message(embed=utils.embed_success(f'Deleted {number} message(s)'), ephemeral=True)
        await interaction.channel.purge(limit=number) 


# --------------------------------- /inrole (this is horrible but we ball)
    @app_commands.command(name='inrole', description='view users inside a role')
    @app_commands.describe(
        role_name1="Name of the first role",
        role_name2="Name of the second role",
        role_name3="Name of the third role"
    )
    async def list_role_members(
        self, 
        interaction: discord.Interaction, 
        role_name1: str, 
        role_name2: Optional[str] = None, 
        role_name3: Optional[str] = None
    ):
        guild = interaction.guild
        role_mentions = [role_name1, role_name2, role_name3]
        roles = []

        # Filter out None values
        role_mentions = [mention for mention in role_mentions if mention]


        # Find roles and handle errors
        for mention in role_mentions:
            role_id = int(mention.strip('<@&>'))  # Extract role ID from mention
            role = discord.utils.get(guild.roles, id=role_id)
            if not role:
                await interaction.response.send_message(f"Role not found: {mention}", ephemeral=True)
                return
            roles.append(role)

        user_roles = {}
        for role in roles:
            for member in role.members:
                if member.name not in user_roles:
                    user_roles[member.name] = []
                user_roles[member.name].append(role.name)


        user_count = len(user_roles)
        title = f"Members with "+", ".join(role.name for role in roles) ({user_count})
        embed = discord.Embed(title=title, color=roles[0].color)  # Use color of first role

        if not user_roles:
            embed.description = "There are currently no members in any of these roles."
        else:
            if len(roles)>1:
                user_list = "\n".join(f"{username}:\n    {', '.join(user_roles[username])}" for username in sorted(user_roles.keys()))
            else:
                user_list = "\n".join(f"{username}" for username in sorted(user_roles.keys()))
            embed.add_field(name="Users", value=user_list)

        await interaction.response.send_message(embed=embed)

    @list_role_members.autocomplete('role_name1')
    @list_role_members.autocomplete('role_name2')
    @list_role_members.autocomplete('role_name3')
    async def autocomplete_roles(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        guild = interaction.guild
        roles = guild.roles
        matching_roles = [
            app_commands.Choice(name=role.name, value=role.mention)
            for role in roles if current.lower() in role.name.lower()
        ]
        return matching_roles[:10]

# --------------------------------- /.sync_general  (sync commands you dummy)
    @commands.command()
    async def sync_general(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1155194688375103592))
            await ctx.send(f"synced {len(synced)} General commands")
        except discord.HTTPException as er:
            await ctx.send(er)

async def setup(bot):
    await bot.add_cog(General(bot), guilds=[discord.Object(id=1155194688375103592)])
