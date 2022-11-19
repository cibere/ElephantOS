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

FontColorFromTheme = {"light": (255, 255, 255), "dark": (0, 0, 0)}


def _pil_stuff(
    _bytes, timezone: timezone, theme: Literal["light", "dark"]
) -> discord.File:
    image = Image.open(BytesIO(_bytes))
    image = image.resize((750, 1334))

    uiImage = Image.open(f"assets/{theme}_theme.png")
    image.paste(uiImage, (0, 0), uiImage)

    now = datetime.datetime.now(timezone).strftime("%H:%M").split(":")
    if int(now[0]) > 12:
        now[0] = str(int(now[0]) - 12)
        now.append("pm")
    else:
        now.append("am")
    now = f"{now[0]}:{now[1]} {now[2]}"

    draw = ImageDraw.Draw(image)
    myFont = ImageFont.truetype("assets/font.ttf", 30)
    draw.text((320, 18), now, font=myFont, fill=FontColorFromTheme[theme])

    output_buffer = BytesIO()
    image.save(output_buffer, "png")
    output_buffer.seek(0)
    file = discord.File(fp=output_buffer, filename="my_file.png")
    return file


class MainCmds(commands.Cog):
    bot: PhoneBot

    def __init__(self, bot):
        self.bot = bot

    @ap.command(name="open", description="lets you open your phone")
    async def _open(self, inter: discord.Interaction):
        theme = "light"
        _bytes = await self.bot.session.get(
            "https://cdn.discordapp.com/attachments/1014754819493339186/1043391122787008513/my_file.png"
        )
        _bytes = await _bytes.read()
        tz = timezone(timedelta(hours=-8.0))
        func = partial(_pil_stuff, _bytes, tz, theme)
        img = await self.bot.loop.run_in_executor(None, func)
        await inter.response.send_message(file=img)


async def setup(bot):
    await bot.add_cog(MainCmds(bot))
