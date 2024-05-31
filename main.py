import discord
import os
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv

class NEMO(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=intents,
            help_command=None,
            command_prefix='!h'
            )
        self.initial_extensions = [
            "cogs.gather",
            "cogs.produce",
            "cogs.put",
            "cogs.remove",
            "cogs.list",
            "cogs.buy",
            "cogs.trade",
            "cogs.tell",
            "cogs,invite"
        ]

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = NEMO()
bot.run(TOKEN)