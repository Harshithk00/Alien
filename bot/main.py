import asyncio
from bot.bot import DiscordBot
from bot.config import Config


def main():
    bot = DiscordBot()

    async def run_bot():
        await bot.start(Config.TOKEN)

    asyncio.run(run_bot())


if __name__ == '__main__':
    main()