import discord
from discord import app_commands as ap
from discord.ext import commands

from bot import PhoneBot


class ConfigCog(commands.Cog):
    bot: PhoneBot

    def __init__(self, bot):
        self.bot = bot

    config = ap.Group(name="config", description="...")

    @config.command(
        name="background-image", description="lets you customize your background image"
    )
    async def config_bg_image(
        self, inter: discord.Interaction, new_image: discord.Attachment
    ):
        file = await new_image.to_file()
        await inter.response.send_message(file=file)


async def setup(bot: PhoneBot):
    await bot.add_cog(ConfigCog(bot))
