from discord.ext import commands
import modules.db_utils as db_utils
import dotenv

class Initializer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot