# cogs/pull_data.py
import discord
from discord.ext import commands
from discord import app_commands
from bot_config import SERVER_ID, SHEET_NAME, GOOGLE_CREDS_PATH
import gspread
from google.oauth2.service_account import Credentials
import asyncio

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

CURRENT_COLUMNS = ["D", "I", "N", "S"]
BIS_COLUMNS = ["B", "G", "L", "Q"]

# Define the cell ranges for each character (top row)
CHARACTER_CONFIGS_TOP = [
    {"name_cell": "B4", "current_col": CURRENT_COLUMNS[0], "bis_col": BIS_COLUMNS[0]},  # Character 1
    {"name_cell": "G4", "current_col": CURRENT_COLUMNS[1], "bis_col": BIS_COLUMNS[1]},  # Character 2
    {"name_cell": "L4", "current_col": CURRENT_COLUMNS[2], "bis_col": BIS_COLUMNS[2]},  # Character 3
    {"name_cell": "Q4", "current_col": CURRENT_COLUMNS[3], "bis_col": BIS_COLUMNS[3]},  # Character 4
]

# Define the cell ranges for each character (bottom row)
CHARACTER_CONFIGS_BOTTOM = [
    {"name_cell": "B31", "current_col": CURRENT_COLUMNS[0], "bis_col": BIS_COLUMNS[0]},  # Character 5
    {"name_cell": "G31", "current_col": CURRENT_COLUMNS[1], "bis_col": BIS_COLUMNS[1]},  # Character 6
    {"name_cell": "L31", "current_col": CURRENT_COLUMNS[2], "bis_col": BIS_COLUMNS[2]},  # Character 7
    {"name_cell": "Q31", "current_col": CURRENT_COLUMNS[3], "bis_col": BIS_COLUMNS[3]},  # Character 8
]

# Gear slot rows for top characters
GEAR_ROWS = range(7, 20)            # Rows 7-19

# For bottom characters
GEAR_ROWS_BOTTOM = range(34, 47)    # Rows 34-46

GEAR_SLOT_NAMES = [
    "Weapon", "Off-hand", "Head", "Chest", "Gloves", "Pants", "Boots",
    "Earring", "Necklace", "Bracelet", "Ring1", "Ring2"
]

class GearSheetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        creds = Credentials.from_service_account_file(GOOGLE_CREDS_PATH, scopes=SCOPES)
        self.gspread_client = gspread.authorize(creds)
    
    async def fetch_sheet_data(self, sheet_name: str):
        """Fetch and parse the gear sheet"""
        loop = asyncio.get_event_loop()
        
        def _fetch():
            sheet = self.gspread_client.open(sheet_name).sheet1
            
            # GET THE ENTIRE SHEET IN ONE API CALL
            all_values = sheet.get_all_values()
            
            all_characters = []
            
            # Parse top row of characters (1-4)
            for config in CHARACTER_CONFIGS_TOP:
                char_data = self._parse_character(all_values, config, GEAR_ROWS)
                if char_data["name"]:
                    all_characters.append(char_data)
            
            # Parse bottom row of characters (5-8)
            for config in CHARACTER_CONFIGS_BOTTOM:
                char_data = self._parse_character(all_values, config, GEAR_ROWS_BOTTOM)
                if char_data["name"]:
                    all_characters.append(char_data)
            
            return all_characters
        
        data = await loop.run_in_executor(None, _fetch)
        return data

    def _parse_character(self, all_values, config, rows):
        """Parse a single character's gear data from the 2D array"""
        # Convert cell notation (like "B2") to row/col indices
        def cell_to_index(cell):
            """Convert 'B2' to (row_idx, col_idx) - zero-indexed"""
            col = ord(cell[0]) - ord('A')   # B -> 1
            row = int(cell[1:]) - 1         # 2 -> 1 (zero-indexed)
            return row, col
        
        # Get character name
        name_row, name_col = cell_to_index(config["name_cell"])
        char_name = all_values[name_row][name_col] if name_row < len(all_values) and name_col < len(all_values[name_row]) else "Unknown"
        
        # Get character ilvl
        ilvl_row, ilvl_col = name_row + 1, name_col # TODO: Put this in the config rather than calculating based on name position
        ilvl = all_values[ilvl_row][ilvl_col] if ilvl_row < len(all_values) and ilvl_col < len(all_values[ilvl_row]) else "Unknown"
        
        # Get column index for current and BiS gear
        current_col = ord(config["current_col"]) - ord('A')
        bis_col = ord(config["bis_col"]) - ord('A')
        
        # Get current gear
        current_gear = {}
        for i, row in enumerate(rows):
            if i < len(GEAR_SLOT_NAMES):
                row_idx = row - 1  # Convert to zero-indexed
                cell_value = all_values[row_idx][current_col] if row_idx < len(all_values) and current_col < len(all_values[row_idx]) else "Empty"
                current_gear[GEAR_SLOT_NAMES[i]] = cell_value or "Empty"
        
        # Get BiS gear
        bis_gear = {}
        for i, row in enumerate(rows):
            if i < len(GEAR_SLOT_NAMES):
                row_idx = row - 1  # Convert to zero-indexed
                cell_value = all_values[row_idx][bis_col] if row_idx < len(all_values) and bis_col < len(all_values[row_idx]) else "Empty"
                bis_gear[GEAR_SLOT_NAMES[i]] = cell_value or "Empty"
        
        return {
            "name": char_name,
            "ilvl": ilvl,
            "current": current_gear,
            "bis": bis_gear
        }
    
    @app_commands.command(
            name="pullgear", 
            description="Pull gear data from Google Sheets")
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def pull_gear(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            data = await self.fetch_sheet_data(SHEET_NAME)
            
            # Create embed to display the data
            embed = discord.Embed(
                title="📊 Gear Data Retrieved",
                description=f"Successfully pulled data for {len(data)} characters",
                color=discord.Color.green()
            )
            
            for char in data:
                # Show current gear summary
                current_summary = ", ".join([f"{slot}: {gear}" for slot, gear in list(char["current"].items())[:3]])
                bis_summary = ", ".join([f"{slot}: {gear}" for slot, gear in list(char["bis"].items())[:3]])
                embed.add_field(
                    name=f"✅ {char['name']}",
                    value=f"**Current**: {current_summary}\n**BiS**: {bis_summary}\n**iLvL**: {char["ilvl"]}",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed)
            
            print(f"\nSuccessfully pulled gear for {len(data)} characters")
            # for char in data:
            #     print(f"\n{char['name']}:")
            #     print(f"  Current: {char['current']}")
            #     print(f"  BiS: {char['bis']}")
            
        except Exception as e:
            await interaction.followup.send(f"❌ Error fetching data: {e}", ephemeral=True)
            print(f"Full error: {e}")
            import traceback
            traceback.print_exc()

async def setup(bot):
    await bot.add_cog(GearSheetCog(bot))