import os
import time  # Added time import
import discord
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot client
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    print(f'Logged in as {client.user}')
    print('------')


@client.event
async def on_message(message):
    """Respond to messages"""
    # Prevent bot from responding to its own messages
    if message.author == client.user:
        return

    # Simple ping response
    if message.content.lower() == '!ping':
        # Record start time
        start_time = time.time()

        # Send initial ping message
        ping_message = await message.channel.send('Pinging...')

        # Calculate latency
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)

        # Calculate Discord API latency
        api_latency = round(client.latency * 1000, 2)

        # Edit the message with detailed ping information
        await ping_message.edit(content=f"""
🏓 Pong!
• Message Latency: `{latency} ms`
• API Latency: `{api_latency} ms`
        """)


# Run the bot
def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: No Discord token found. Check your .env file.")
        return

    client.run(token)


if __name__ == '__main__':
    main()