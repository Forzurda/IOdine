import discord
from discord.ext import commands
from discord import app_commands
from pprint import pprint

# Constants
TARGET_CHANNEL_ID = 1209821638422564864  # Quali Channel ID
ALLOWED_ROLES = ["Staff", "Moderator", "Admin", "Owner", "Dev"]  # Replace with your allowed role names
HARDCODED_ROLE_NAME = "Ready"  # The role to be assigned by the button

class RoleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label=f"Ready", style=discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        new_role = discord.utils.get(guild.roles, name=HARDCODED_ROLE_NAME)

        if new_role is not None:
            # Remove any existing roles from the selection roles
            await member.remove_roles(*[role for role in member.roles if role.name == HARDCODED_ROLE_NAME])

            # Add the new role
            await member.add_roles(new_role)
            await interaction.response.send_message(f'Registered your participation ✅', ephemeral=True, delete_after=5.0)
            pprint(f'{interaction.user} selected {new_role}.')
        else:
            await interaction.response.send_message(f'The role {HARDCODED_ROLE_NAME} does not exist.', ephemeral=True)

class RoleButtonView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(RoleButton())

class RoleButtonMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        pprint('RoleButtonMenu cog loaded')

    async def remove_role_from_all_members(self, guild: discord.Guild, role_name: str):
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            for member in guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
                    pprint(f'Removed {role} from {member}')

    @app_commands.command(name="ready_check_send", description="Send a ready check message with a button")
    @commands.has_any_role(*ALLOWED_ROLES)  # Restrict command to specific roles
    async def menu(self, interaction: discord.Interaction):
        # Fetch the target channel
        target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
        if target_channel is None:
            await interaction.response.send_message(f"Target channel with ID {TARGET_CHANNEL_ID} not found.", ephemeral=True)
            return

        # Remove the hardcoded role from all members
        await self.remove_role_from_all_members(interaction.guild, HARDCODED_ROLE_NAME)
        
        embed = discord.Embed(title="Ready Check", colour=0x00c1f1)
        embed.add_field(name="", value=f"Click the button below to confirm your participation!")
        await target_channel.send(embed=embed, view=RoleButtonView())
        await interaction.response.send_message(f"Message sent to {target_channel.mention}, and {HARDCODED_ROLE_NAME} removed from all users.")
    
    @commands.command()
    @commands.has_any_role(*ALLOWED_ROLES)  # Restrict command to specific roles
    async def sync_readyc(self, ctx):
        try:
            guild = discord.Object(id=1077859376414593124)  # Replace with your guild ID
            self.bot.tree.copy_global_to(guild=guild)
            synced = await self.bot.tree.sync(guild=guild)
            await ctx.send(f"Synced {len(synced)} ReadyCheck command.")
        except discord.HTTPException as er:
            await ctx.send(f"Failed to sync commands: {er}")

async def setup(bot):
    await bot.add_cog(RoleButtonMenu(bot))
