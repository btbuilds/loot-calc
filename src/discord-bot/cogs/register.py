# cogs/register.py
import discord
from discord.ext import commands
from discord import app_commands
from bot_config import SERVER_ID
#from database import add_player

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="register", 
        description="Register your character for the loot tracker."
    )
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def register(self, interaction: discord.Interaction, character_name: str):
        # add_player(interaction.user.id, character_name) TODO: Implement this in the database
        await interaction.response.send_message(f"Registered as {character_name}!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Register(bot))