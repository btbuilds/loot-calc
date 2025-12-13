bot_config.py structure:

import os

BOT_TOKEN = "a1b2c3" # your bot token from Discord
SERVER_ID = 1234 # your guild ID from Discord
SHEET_NAME = "Arcadion Heavyweight" # Sheet name that was shared with the project in google cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CREDS_PATH = os.path.join(BASE_DIR, "credentials.json") # store the credentials.json in the same location as bot_config