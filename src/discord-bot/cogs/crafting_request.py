# cogs/crafting_request.py
import discord
from discord.ext import commands
from discord import app_commands
from bot_config import SERVER_ID

# ----- UI COMPONENTS -----

class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Gear",
                description="I hear it's inappropriate to be naked."
            ),
            discord.SelectOption(
                label="Food",
                description="Om nom nom."
            ),
            discord.SelectOption(
                label="Potion",
                description="We chugging that shit."
            ),
            discord.SelectOption(
                label="Other",
                description="Is there other stuff to craft? idk"
            )
        ]

        super().__init__(
            placeholder="What do you need crafted?",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]

        if choice == "Gear":
            await interaction.response.send_message(
                f"You selected {choice}. Now we can offer combat/crafting/etc.",
                ephemeral=True
            )
        elif choice == "Food":
            await interaction.response.send_message(
                f"You selected {choice}. Which food do they want?",
                ephemeral=True
            )
        elif choice == "Potion":
            await interaction.response.send_message(
                f"You selected {choice}. Which potion? Str/Dex/Int?",
                ephemeral=True
            )
        elif choice == "Other":
            await interaction.response.send_message(
                f"You selected {choice}. Are there other categories someone could want? Housing?",
                ephemeral=True
            )


class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

# ----- COG -----

class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="craft_request",
        description="Show the crafting request menu."
    )
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def menu_cmd(self, interaction: discord.Interaction):
        """Sends the menu with the dropdown options."""
        view = MenuView()
        await interaction.response.send_message("Choose an option:", view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(MenuCog(bot))