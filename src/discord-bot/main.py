import discord
from discord.ext import commands
from bot_config import BOT_TOKEN, SERVER_ID

GUILD_ID = discord.Object(id=SERVER_ID)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class Client(commands.Bot):
    async def setup_hook(self):
        # Load cogs on startup
        for ext in [
            "cogs.crafting_request",
            "cogs.register",
            "cogs.test_commands"  # Add your new test commands cog
        ]:
            await self.load_extension(ext)

        # Guild-based slash command sync
        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to guild {GUILD_ID}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_ready(self):
        print(f'Logged on as {self.user}')

client = Client(command_prefix="!", intents=intents)

client.run(BOT_TOKEN)