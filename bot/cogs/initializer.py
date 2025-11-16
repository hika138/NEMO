"""
Initializer Cog
"""

from discord.ext import commands

class Initializer(commands.Cog):
    """
    Initializer Cog
    
    Args:
        bot (commands.Bot): The bot instance
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
