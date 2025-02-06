import time
from discord.ext import commands


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Check bot's latency"""
        start_time = time.time()

        # Send initial ping message
        ping_message = await ctx.send('Pinging...')

        # Calculate latency
        end_time = time.time()
        message_latency = round((end_time - start_time) * 1000, 2)
        api_latency = round(self.bot.latency * 1000, 2)

        # Edit the message with detailed ping information
        await ping_message.edit(content=f"""
🏓 Pong!
• Message Latency: `{message_latency} ms`
• API Latency: `{api_latency} ms`
        """)


async def setup(bot):
    await bot.add_cog(PingCog(bot))