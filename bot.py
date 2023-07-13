import asyncio
import os
import discord
import openai

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        try:
            synced = await client.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            await client.change_presence(activity=discord.Game('Minecraft'))
        except Exception as e:
            print(e)

    @client.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

    @client.tree.command(name="talk")
    @app_commands.describe(message = "What should I say?")
    async def talk(interaction: discord.Interaction, message: str):
        userInfo = (f"{interaction.user.mention} asked: {message}. ChatNix replied: \n")
        await interaction.response.defer()
        await asyncio.sleep(delay=0)
        await interaction.followup.send(chatgpt_message(userInfo, message))
        
    client.run(DISCORD_TOKEN)

def chatgpt_message(userInfo:str, message: str):
    openai.api_key = OPENAI_TOKEN
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
    response_message = userInfo
    response_message += completion.choices[0].message.content
    return response_message


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    OPENAI_TOKEN = os.getenv('OPENAI_API_KEY')
    main()