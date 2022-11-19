from functools import partial
from io import BytesIO

import discord
from discord import app_commands as ap
from discord.ext import commands
from PIL import Image

from bot import PhoneBot


def _pil_stuff(_bytes) -> discord.File:
    image = Image.open(BytesIO(_bytes))
    image = image.resize((750, 1334))

    uiImage = Image.open("assets/default.png")
    # Image.Image.paste(image, uiImage, (0, 0))

    output_buffer = BytesIO()
    image.save(output_buffer, "png")
    output_buffer.seek(0)
    file = discord.File(fp=output_buffer, filename="my_file.png")
    return file


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
        if not "image" in str(new_image.content_type):
            return await inter.response.send_message(
                "You can only set images to your background image", ephemeral=True
            )
        _bytes = await new_image.read()
        func = partial(_pil_stuff, _bytes)
        img = await self.bot.loop.run_in_executor(None, func)
        await inter.response.send_message(file=img)


async def setup(bot: PhoneBot):
    await bot.add_cog(ConfigCog(bot))
