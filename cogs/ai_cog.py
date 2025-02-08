import discord
import itertools
import asyncio
from discord.ext import commands
from utils.gemini_chat import GeminiChat  # Import the GeminiChat utility


class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gemini_chat = GeminiChat()
        self.user_chat_histories = {}  # Chat history per user

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot's own messages or non-guild messages
        if message.author == self.bot.user or message.guild is None:
            return

        # Trigger when the bot is mentioned
        if self.bot.user.mentioned_in(message):
            clean_message = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            user_id = message.author.id

            # Ensure chat history exists for the user
            if user_id not in self.user_chat_histories:
                self.user_chat_histories[user_id] = []

            # Generate response using GeminiChat
            response = self.gemini_chat.generate_response(clean_message, self.user_chat_histories[user_id])

            # Update chat history
            self.user_chat_histories[user_id].append({"role": "user", "content": clean_message})
            self.user_chat_histories[user_id].append({"role": "model", "content": response})

            await message.channel.send(response)

    # @commands.command(name="ask", aliases=["ai", "chat"])
    # async def ask(self, ctx, *, query):
    #     """Command to ask the bot a question."""
    #     user_id = ctx.author.id
    #
    #     # Ensure chat history exists for the user
    #     if user_id not in self.user_chat_histories:
    #         self.user_chat_histories[user_id] = []
    #
    #     response = self.gemini_chat.generate_response(query, self.user_chat_histories[user_id])
    #     self.user_chat_histories[user_id].append({"role": "user", "content": query})
    #     self.user_chat_histories[user_id].append({"role": "model", "content": response})
    #
    #     await ctx.send(response)

    # @commands.command(name="ask", aliases=["ai", "chat"])
    # async def ask(self, ctx, *, query):
    #     """Command to ask the bot a question with loading indicator."""
    #     user_id = ctx.author.id
    #
    #     # Start typing indicator
    #     async with ctx.typing():
    #         try:
    #             # Ensure chat history exists for the user
    #             if user_id not in self.user_chat_histories:
    #                 self.user_chat_histories[user_id] = []
    #
    #             # Generate response using GeminiChat
    #             # Use asyncio.to_thread to prevent blocking
    #             response = await asyncio.to_thread(
    #                 self.gemini_chat.generate_response,
    #                 query,
    #                 self.user_chat_histories[user_id]
    #             )
    #
    #             # Update chat history
    #             self.user_chat_histories[user_id].append({"role": "user", "content": query})
    #             self.user_chat_histories[user_id].append({"role": "model", "content": response})
    #
    #             # Send the response
    #             await ctx.send(response)
    #
    #         except Exception as e:
    #             # Handle any errors
    #             error_message = f"Sorry, I encountered an error: {str(e)}"
    #             await ctx.send(error_message)

    @commands.command(name="ask", aliases=["ai", "chat"])
    async def ask(self, ctx, *, query):
        # Send an initial loading message
        loading_msg = await ctx.send("🤔 Thinking...")

        try:
            # Generate response
            response = await asyncio.to_thread(
                self.gemini_chat.generate_response,
                query,
                self.user_chat_histories.get(ctx.author.id, [])
            )

            # Edit the loading message with the response
            await loading_msg.edit(content=response)

        except Exception as e:
            await loading_msg.edit(content=f"❌ Error: {str(e)}")

    # @commands.command(name="ask", aliases=["ai", "chat"])
    # async def ask(self, ctx, *, query):
    #     # Animated loading indicators
    #     loading_icons = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕"]
    #
    #     # Send initial loading message
    #     loading_msg = await ctx.send(loading_icons[0])
    #
    #     try:
    #         # Animate loading
    #         for icon in itertools.cycle(loading_icons):
    #             # Set a timeout to prevent infinite animation
    #             try:
    #                 response = await asyncio.wait_for(
    #                     asyncio.to_thread(
    #                         self.gemini_chat.generate_response,
    #                         query,
    #                         self.user_chat_histories.get(ctx.author.id, [])
    #                     ),
    #                     timeout=30.0  # 30 seconds timeout
    #                 )
    #                 break
    #             except asyncio.TimeoutError:
    #                 await loading_msg.edit(content=f"{icon} Still thinking...")
    #
    #         # Send final response
    #         await loading_msg.edit(content=response)
    #
    #     except Exception as e:
    #         await loading_msg.edit(content=f"❌ Error: {str(e)}")

    @commands.command(name="clearhistory")
    async def clear_history(self, ctx):
        """Command to clear chat history for the user."""
        user_id = ctx.author.id

        if user_id in self.user_chat_histories:
            self.user_chat_histories[user_id] = []
            await ctx.send("Your chat history has been cleared.")
        else:
            await ctx.send("You don't have any chat history to clear.")


async def setup(bot):
    await bot.add_cog(AICog(bot))