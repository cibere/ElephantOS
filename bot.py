import logging
import logging.handlers
import traceback

import asqlite
import ciberedev
import discord
from aiohttp import ClientSession
from discord.ext import commands


class colorFormatters:
    class discord(logging.Formatter):
        LEVEL_COLOURS = [
            (logging.DEBUG, "\x1b[40;1m"),
            (logging.INFO, "\x1b[34;1m"),
            (logging.WARNING, "\x1b[33;1m"),
            (logging.ERROR, "\x1b[31m"),
            (logging.CRITICAL, "\x1b[41m"),
        ]

        FORMATS = {
            level: logging.Formatter(
                f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            for level, colour in LEVEL_COLOURS
        }

        def format(self, record):
            formatter = self.FORMATS.get(record.levelno)
            if formatter is None:
                formatter = self.FORMATS[logging.DEBUG]
            if record.exc_info:
                text = formatter.formatException(record.exc_info)
                record.exc_text = f"\x1b[31m{text}\x1b[0m"

            output = formatter.format(record)
            record.exc_text = None
            return output

    class main(logging.Formatter):
        LEVEL_COLOURS = [
            (logging.DEBUG, "\x1b[40;1m"),
            (logging.INFO, "\x1b[34;1m"),
            (logging.WARNING, "\x1b[33;1m"),
            (logging.ERROR, "\x1b[31m"),
            (logging.CRITICAL, "\x1b[41m"),
        ]

        FORMATS = {
            level: logging.Formatter(
                f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            for level, colour in LEVEL_COLOURS
        }

        def format(self, record):
            formatter = self.FORMATS.get(record.levelno)
            if formatter is None:
                formatter = self.FORMATS[logging.DEBUG]
            if record.exc_info:
                text = formatter.formatException(record.exc_info)
                record.exc_text = f"\x1b[31m{text}\x1b[0m"

            output = formatter.format(record)
            record.exc_text = None
            return output


discordLogger = logging.getLogger("discord")
discordLogger.setLevel(20)
log_handler = logging.StreamHandler()
log_handler.setFormatter(colorFormatters.discord())
discordLogger.addHandler(log_handler)

mainLogger = logging.getLogger("main")
mainLogger.setLevel(20)
log_handler = logging.StreamHandler()
log_handler.setFormatter(colorFormatters.main())
mainLogger.addHandler(log_handler)


class loggers:
    def __init__(self):
        self.discord = discordLogger
        self.main = mainLogger


class PhoneBot(commands.Bot):
    session: ClientSession
    user: discord.ClientUser

    def __init__(self):
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        super().__init__(
            command_prefix=commands.when_mentioned, help_command=None, intents=intents
        )
        self.cdev = ciberedev.Client()
        self.modules = ["cogs.config", "cogs.open_cmd", "devcmd"]
        self.loggers = loggers()

    async def setup_hook(self) -> None:
        async with asqlite.connect("data.db") as con:
            async with con.cursor() as cur:
                await cur.execute(
                    "CREATE TABLE IF NOT EXISTS config (id INT, backgroundImage BYTES, timezone TEXT)"
                )
                await cur.execute(
                    "CREATE TABLE IF NOT EXISTS texts (id INT, reciever INT, sender INT, content TEXT)"
                )
                await con.commit()

        for module in self.modules:
            try:
                await self.load_extension(module)
            except:
                error = traceback.format_exc()
                self.loggers.main.exception(
                    f"Ignoring Exception while loading {module}\n{error}"
                )
        self.loggers.main.info("setup_hook finished")

    async def on_ready(self):
        self.loggers.main.info(
            f"on_ready ran, logged in as {self.user} ({self.user.id})"
        )
