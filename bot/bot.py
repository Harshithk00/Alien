import discord
from discord.ext import commands
from bot.config import Config


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents
        )

    async def setup_hook(self):
        # Load cogs (extensions)
        await self.load_extension('cogs.ping')
        # Add more cogs as you develop them
        print(f"Logged in as {self.user}")

    async def on_ready(self):
        print(f'Bot is ready. Logged in as {self.user}')