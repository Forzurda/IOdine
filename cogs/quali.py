import discord
from discord.ext import commands
from discord import app_commands
from pprint import pprint

# Role mapping dictionary
SELECTION_ROLE_MAP = {
    "Q-1": "Q-1",
    "Q-2": "Q-2",
    "Q-3": "Q-3",
    "Q-4": "Q-4",
    "Q-5": "Q-5",
    "Q-6": "Q-6",
    "Q-7": "Q-7",
    "Q-8": "Q-8",
    "Q-9": "Q-9",
    "Q-10": "Q-10"
}

TARGET_CHANNEL_ID = 1224169292077994014  # Quali Channel ID
ALLOWED_ROLES = ["Staff", "Moderator", "Admin", "Owner", "Dev"]  # Replace with your allowed role names

class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Q-1"),
            discord.SelectOption(label="Q-2"),
            discord.SelectOption(label="Q-3"),
            discord.SelectOption(label="Q-4"),
            discord.SelectOption(label="Q-5"),
            discord.SelectOption(label="Q-6"),
            discord.SelectOption(label="Q-7"),
            discord.SelectOption(label="Q-8"),
            discord.SelectOption(label="Q-9"),
            discord.SelectOption(label="Q-10")
        ]
        super().__init__(placeholder="Select a qualifying session", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]
        new_role_name = SELECTION_ROLE_MAP[selected_value]
        
        guild = interaction.guild
        member = interaction.user
        new_role = discord.utils.get(guild.roles, name=new_role_name)

        if new_role is not None:
            # Remove any existing roles from the selection roles
            existing_roles = [discord.utils.get(guild.roles, name=role_name) for role_name in SELECTION_ROLE_MAP.values()]
            await member.remove_roles(*[role for role in existing_roles if role in member.roles])

            # Add the new role
            await member.add_roles(new_role)
            await interaction.response.send_message(f'You selected {selected_value} and have been assigned the role {new_role_name}.', ephemeral=True)
            pprint(f'{interaction.user} selected {new_role}.')
        else:
            await interaction.response.send_message(f'The role {new_role_name} does not exist.', ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class SelectMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        pprint('QualiMessage cog loaded')

    @app_commands.command(name="qualifying_menu_send", description="Send a qualifying time with menu select")
    @commands.has_any_role(*ALLOWED_ROLES)  # Restrict command to specific roles
    async def menu(self, interaction: discord.Interaction):
        # Fetch the target channel
        target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
        if target_channel is None:
            await interaction.response.send_message(f"Target channel with ID {TARGET_CHANNEL_ID} not found.", ephemeral=True)
            return
        
        embed = discord.Embed(title="Qualifying Timeslots", colour=0x00c1f1)
        embed.set_thumbnail(url="https://probot.media/PoQSKyH6MN.png")
        embed.add_field(name="Sign up to a Qualifying Session for R5 of the RHEC here by selecting a session in the dropdown menu.", 
                        value=("Q-1: <t:1717776000:F>, <t:1717776000:R>\n  \
                                Q-2: <t:1717783200:F>, <t:1717783200:R>\n   \
                                Q-3: <t:1717790400:F>, <t:1717790400:R>\n   \
                                Q-4: <t:1717797600:F>, <t:1717797600:R>\n   \
                                Q-5: <t:1717812000:F>, <t:1717812000:R>\n   \
                                Q-6: <t:1717826400:F>, <t:1717826400:R>\n   \
                                Q-7: <t:1717833600:F>, <t:1717833600:R>\n   \
                                Q-8: <t:1717833600:F>, <t:1717833600:R>\n   \
                                Q-9: <t:1717862400:F>, <t:1717862400:R>\n   \
                                Q-10: <t:1717876800:F>, <t:1717876800:R>\n"))
        await target_channel.send(embed=embed, view=SelectView())
        await interaction.response.send_message(f"Message sent to {target_channel.mention}.")
    
    @commands.command()
    @commands.has_any_role(*ALLOWED_ROLES)  # Restrict command to specific roles
    async def sync_quali(self, ctx):
        try:
            guild = discord.Object(id=1077859376414593124)  # Replace with your guild ID
            self.bot.tree.copy_global_to(guild=guild)
            synced = await self.bot.tree.sync(guild=guild)
            await ctx.send(f"Synced {len(synced)} QualiMessage command.")
        except discord.HTTPException as er:
            await ctx.send(f"Failed to sync commands: {er}")

async def setup(bot):
    await bot.add_cog(SelectMenu(bot))
