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
            "cogs.register"
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

class View(discord.ui.View):
    @discord.ui.button(label="Click Here", style=discord.ButtonStyle.primary, emoji="🍑")
    async def button_callback(self, button, interaction):
        await button.response.send_message("BUTTon clicked.", ephemeral=True)

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

@client.tree.command(name="hello", description="Just says hello", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello")

@client.tree.command(name="printer", description="Prints arguments", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="embed", description="Embed test", guild=GUILD_ID)
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="This is a title", description="This is a description", color=discord.Color.dark_purple())
    embed.set_thumbnail(url="https://img.icons8.com/dusk/1200/final-fantasy-xiv.jpg")
    embed.add_field(name="A stinky embed", value="We getting there though", inline=False)
    embed.add_field(name="Second line", value="This should appear on the second line.", inline=True)
    embed.add_field(name="Second line as well", value="Also on second line", inline=True)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="secret_embed", description="Ephemeral embed test", guild=GUILD_ID)
async def secret_embed(interaction: discord.Interaction):
    embed = discord.Embed(title="This is a title", description="This is a description", color=discord.Color.dark_purple())
    embed.set_thumbnail(url="https://img.icons8.com/dusk/1200/final-fantasy-xiv.jpg")
    embed.add_field(name="A stinky embed", value="We getting there though", inline=False)
    embed.add_field(name="Second line", value="This should appear on the second line.", inline=True)
    embed.add_field(name="Second line as well", value="Also on second line", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="buttons", description="Testing buttons", guild=GUILD_ID)
async def button(interaction: discord.Interaction):
    await interaction.response.send_message(view=View(), ephemeral=True)

@client.tree.command(name="dropdown", description="Show a dropdown menu", guild=GUILD_ID)
async def dropdown(interaction:discord.Interaction):
    await interaction.response.send_message(view=MenuView(), ephemeral=True)

client.run(BOT_TOKEN)