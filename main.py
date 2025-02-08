import os


# import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "/"

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

if BOT_TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set in the .env file or is invalid")


async def load_cogs():
    """Load all bot cogs (features)."""
    await bot.load_extension("cogs.ai_cog")  # Path to AI cog (cogs/ai_cog.py)


@bot.event
async def on_ready():
    """Event triggered when bot is online."""
    print(f"Bot is online! Logged in as {bot.user}")
    print("Ready to chat!")


# Main entry point
async def main():
    await load_cogs()
    await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())