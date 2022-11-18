import asyncio

from aiohttp import ClientSession

from bot import PhoneBot

bot = PhoneBot()


async def main(token):
    async with ClientSession() as cs, bot.cdev:
        bot.session = cs
        await bot.start(token)


if __name__ == "__main__":
    with open("__token__.txt", "r") as f:
        token = f.read()
    asyncio.run(main(token))
