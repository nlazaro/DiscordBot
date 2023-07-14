import os
import discord
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

class clientBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Game('Minecraft')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.discord_api_key = os.getenv('DISCORD_TOKEN')
        
client = clientBot()