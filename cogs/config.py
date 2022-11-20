import datetime
from datetime import timedelta, timezone
from functools import partial
from io import BytesIO
from typing import Literal

import discord
from discord import app_commands as ap
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

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
        self,
        inter: discord.Interaction,
        new_image: discord.Attachment,
    ):
        return
        if not "image" in str(new_image.content_type):
            return await inter.response.send_message(
                "You can only set images to your background image", ephemeral=True
            )
        _bytes = await new_image.read()
        tz = timezone(timedelta(hours=-8.0))
        func = partial(_pil_stuff, _bytes, tz, theme)
        img = await self.bot.loop.run_in_executor(None, func)
        await inter.response.send_message(file=img)


async def setup(bot: PhoneBot):
    await bot.add_cog(ConfigCog(bot))
