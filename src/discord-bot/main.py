import discord
from discord.ext import commands
from discord import app_commands
from bot_config import BOT_TOKEN, SERVER_ID

GUILD_ID = discord.Object(id=SERVER_ID)

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to guild {GUILD_ID}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True



client = Client(command_prefix="!", intents=intents)

@client.tree.command(name="hello", description="Just says hello", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello")

@client.tree.command(name="printer", description="Prints arguments", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

client.run(BOT_TOKEN)