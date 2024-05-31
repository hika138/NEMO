import discord
import os
from discord import app_commands
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv
from nemo import nemo_player

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
guild_id = os.environ.get('GUILD_ID')

class gather(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.guild = self.bot.get_guild(guild_id)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=self.guild)

    @app_commands.command(
        name="gather",
        description="Gather resources from the environment."
    )
    @app_commands.guilds(guild_id)
    async def gather(self, ctx:discord.Interaction):
        await ctx.response.send_message("Gathering resources...")