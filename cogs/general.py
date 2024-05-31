import discord
import math
from typing import Optional, List
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from discord.utils import *
from cogs.misc.roles import Roles
from cogs.misc import utils

role_ids = Roles()

class EmbedMenu(discord.ui.View):
    def __init__(self, embeds, timeout=None):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.current_page = 0

        if len(embeds) == 1:
            self.remove_item(self.first_page)
            self.remove_item(self.previous_page)
            self.remove_item(self.next_page)
            self.remove_item(self.last_page)
            self.remove_item(self.increment_page)
            self.remove_item(self.decrement_page)

    async def show_page(self, page_number, interaction=None):
        self.current_page = page_number
        embed = self.embeds[page_number]

        if interaction:
            view = self
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            message = self.message
            view = message.view if message else None

            if view:
                view.stop()
            await message.edit(embed=embed, view=self)

    @discord.ui.button(label='\u23EE')
    async def first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page != 0:
            await self.show_page(0, interaction)

    @discord.ui.button(label='\u23EA')  # New button for decrementing -10 pages
    async def decrement_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_page = self.current_page - 10
        if new_page >= 0:
            await self.show_page(new_page, interaction)

    @discord.ui.button(label='\u25C0')
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            await self.show_page(self.current_page - 1, interaction)
        self.current_page - 1

    @discord.ui.button(label='\u25B6')
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.embeds) - 1:
            await self.show_page(self.current_page + 1, interaction)
        self.current_page + 1

    @discord.ui.button(label='\u23E9')  # New button for incrementing +10 pages
    async def increment_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_page = self.current_page + 10
        if new_page < len(self.embeds):
            await self.show_page(new_page, interaction)

    @discord.ui.button(label='\u23ED')
    async def last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page != len(self.embeds) - 1:
            await self.show_page(len(self.embeds) - 1, interaction)


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
    @app_commands.checks.has_permissions(moderate_members=True)
    async def clear(self, interaction: discord.Interaction, number: int):
        await interaction.response.send_message(embed=utils.embed_success(f'Deleted {number} message(s)'), ephemeral=True)
        await interaction.channel.purge(limit=number) 





# --------------------------------- /inrole (this is horrible but we ball)
    @app_commands.command(name='inrole', description='view users inside a role')
    @app_commands.describe(
        role1="Name of the first role",
        role2="Name of the second role",
        role3="Name of the third role"
    )
    async def list_role_members(
        self, 
        interaction: discord.Interaction, 
        role1: discord.Role, 
        role2: discord.Role = None, 
        role3: discord.Role = None
    ):
        guild = interaction.guild
        '''
        - Converted the types for role_names from str to discord.Role type
        - Added a simplified None check for the roles, as a user will not be able to type in a fake role
        - 

        '''
        roles_input = [role1, role2, role3]
        roles_objs = []

        for r in roles_input:
            if r:
                role_objects = discord.utils.get(guild.roles, name=r.name)
                if role_objects:
                    roles_objs.append(role_objects)

        user_roles = {}
        for role in roles_objs:
            for member in role.members:
                if member.name not in user_roles:
                    user_roles[member.name] = []
                user_roles[member.name].append(role.name)

       

        user_count = len(user_roles)
        title = f"({user_count}) Members with "+" or ".join(role.name for role in roles_objs) 
        embed = discord.Embed(title=title, color=roles_objs[0].color)  # Use color of first role
        embeds = []

        if not user_roles:
            embed.description = "There are currently no members in any of these roles."
            await interaction.response.send_message(embed=embed)
        else:
            
            fields = []
            for user, roles in user_roles.items():
                fields.append((user, ", ".join([discord.utils.get(guild.roles, name=role).mention for role in roles])))

            pages = math.ceil(len(fields) / 25)
            for page in range(pages):
                embed = discord.Embed(title=title, color=roles_objs[0].color if roles_objs else discord.Color.default())
                for user, roles in fields[page*25:(page+1)*25]:
                    if len(roles_objs)>1:
                        embed.add_field(name=user, value=roles, inline=False)
                    else:
                        embed.add_field(name=user, value="", inline=False)
                embed.set_footer(text=f"Page {page + 1} of {pages}")
                embeds.append(embed)


            menu = EmbedMenu(embeds)
            menu.message = await interaction.response.send_message(embed=embeds[0], view=menu)

    # @list_role_members.autocomplete('role_name1')
    # @list_role_members.autocomplete('role_name2')
    # @list_role_members.autocomplete('role_name3')
    # async def autocomplete_roles(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    #     guild = interaction.guild
    #     roles = guild.roles
    #     matching_roles = [
    #         app_commands.Choice(name=role.name, value=role.mention)
    #         for role in roles if current.lower() in role.name.lower()
    #     ]
    #     return matching_roles[:10]

# --------------------------------- /.sync_general  (sync commands you dummy)
    
    @commands.command()
    async def sync_general(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync()
            await ctx.send(f"synced {len(synced)} General commands")
        except discord.HTTPException as er:
            await ctx.send(er)

async def setup(bot):
    await bot.add_cog(General(bot))
