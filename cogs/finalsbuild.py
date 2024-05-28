import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc.roles import Roles
import random
import json

role_ids = Roles()

class FinalsBuild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('The Finals Build cog loaded')
 
    
    async def load_build(self):
        with open("JSONS/build.json") as file:
            buildsfile = json.load(file)
            
        builds = buildsfile["builds"]
        build = random.choice(builds)["build"]
        print(f"Build is {build}")
        return build
        


    async def load_gun(self, build: str):
        with open("JSONS/guns.json") as file:
            gunsfile = json.load(file)
            
        guns = gunsfile["guns"]
        specgun = [x for x in guns if build in x.values()]
        gun = random.choice(specgun)["name"]
        print(f"Gun is {gun}")
        return gun




    async def load_gadget(self, build: str):
        with open("JSONS/gadgets.json") as file:
            gadgetsfile = json.load(file)
        pickedgadgets = []   
        gadgets = gadgetsfile["gadgets"]
        specgadget = [x for x in gadgets if build in x.values() or any(build in gadgetbuild for gadgetbuild in x["build"])]
        list_filled = False
        while not list_filled:
            gadget = random.choice(specgadget)["name"]
            if gadget in pickedgadgets:
                continue
            pickedgadgets.append(gadget)
            if len(pickedgadgets) == 4:
                list_filled = True
        print(f"Gadgets is {pickedgadgets}")
        return pickedgadgets




    async def load_spec(self, build: str):
        with open("JSONS/specs.json") as file:
            specsfile = json.load(file)
            
        specs = specsfile["specializations"]
        specspec = [x for x in specs if build in x.values()]
        spec = random.choice(specspec)["name"]
        print(f"Specialization is {spec}")
        return spec

    @app_commands.command(name="finals_build", description="Generate a the finals build")
    async def generate_finals_build(self, interaction: discord.Interaction):
        build = await self.load_build()
        gun = await self.load_gun(build)
        gadget = await self.load_gadget(build)
        spec = await self.load_spec(build)
        
        print(build, gun, gadget, spec)
        
        embed = discord.Embed(title="The Finals Build", colour=0x71DCF6)
        embed.add_field(name="Randomized The Entrance Exam Build xds", value=f"**Build:** {build}\n **Gun:** {gun}\n **Gadgets:** {", ".join(map(str, gadget))}\n **Specialization:** {spec}\n")
        await interaction.response.send_message(embed=embed)
        

async def setup(bot):
    await bot.add_cog(FinalsBuild(bot), guilds=[discord.Object(id=1155194688375103592)])