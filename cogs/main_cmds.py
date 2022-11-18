import discord
from discord import app_commands as ap
from discord.ext import commands

from bot import PhoneBot


class MainCmds(commands.Cog):
    bot: PhoneBot

    def __init__(self, bot):
        self.bot = bot

    @ap.command(name="open", description="lets you open your phone")
    async def _open(self, inter: discord.Interaction):
        pass


async def setup(bot):
    await bot.add_cog(MainCmds(bot))
