import discord
from discord import app_commands
from discord.ext import commands
from bot_config import SERVER_ID

GUILD_ID = discord.Object(id=SERVER_ID)

class View(discord.ui.View):
    @discord.ui.button(label="Click Here", style=discord.ButtonStyle.primary, emoji="🍑")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("BUTTon clicked.", ephemeral=True)

class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Junk",
                description="Any piece of gear from previous patches."
            ),
            discord.SelectOption(
                label="Crafted",
                description="Crafted gear from current patch."
            ),
            discord.SelectOption(
                label="Tome",
                description="Non-upgraded tome gear from current patch."
            ),
            discord.SelectOption(
                label="Upgraded Tome",
                description="Upgraded tome gear from current patch."
            ),
            discord.SelectOption(
                label="Savage",
                description="Savage gear from current patch."
            )
        ]

        super().__init__(placeholder="Select Gear", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You selected {self.values[0]}', ephemeral=True)

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

class TestCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="hello", description="Just says hello")
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello")
    
    @app_commands.command(name="printer", description="Prints arguments")
    async def printer(self, interaction: discord.Interaction, printer: str):
        await interaction.response.send_message(printer)
    
    @app_commands.command(name="embed", description="Embed test")
    async def embed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="This is a title", 
            description="This is a description", 
            color=discord.Color.dark_purple()
        )
        embed.set_thumbnail(url="https://img.icons8.com/dusk/1200/final-fantasy-xiv.jpg")
        embed.add_field(name="A stinky embed", value="We getting there though", inline=False)
        embed.add_field(name="Second line", value="This should appear on the second line.", inline=True)
        embed.add_field(name="Second line as well", value="Also on second line", inline=True)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="secret_embed", description="Ephemeral embed test")
    async def secret_embed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="This is a title", 
            description="This is a description", 
            color=discord.Color.dark_purple()
        )
        embed.set_thumbnail(url="https://img.icons8.com/dusk/1200/final-fantasy-xiv.jpg")
        embed.add_field(name="A stinky embed", value="We getting there though", inline=False)
        embed.add_field(name="Second line", value="This should appear on the second line.", inline=True)
        embed.add_field(name="Second line as well", value="Also on second line", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="buttons", description="Testing buttons")
    async def button(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=View(), ephemeral=True)
    
    @app_commands.command(name="dropdown", description="Show a dropdown menu")
    async def dropdown(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=MenuView(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(TestCommandsCog(bot), guild=GUILD_ID)