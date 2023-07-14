import asyncio
import discord
import openai
from discord.ext import commands
from discord import app_commands
from clientBot import client

def run_bot():
    @client.event
    async def on_ready():
            synced = await client.tree.sync()
            print(f"Synced {len(synced)} commands(s)")
        
    @client.tree.command(name="chat", description="Send a message to ChatGPT")
    async def chat(interaction: discord.Interaction, message: str):
        #   edge case to not reply towards itself
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        await asyncio.sleep(delay=0)
        userInfo = interaction.user.mention
        await interaction.followup.send(chatgpt_message(userInfo, message))
    
    client.run(client.discord_api_key)

def chatgpt_message(userInfo: str, message: str):
    '''
    Args:
        userInfo: The user who sent the message
        message: the message itself
    Returns:
        A reply from chatGPT, which may be a list of messages if the reply exceeds 2000 characters 
    '''
    openai.api_key = client.openai_api_key
    response_message = (f"{userInfo} asked: {message} \n")

    try:
        completion = openai.ChatCompletion.create(
             model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
    except Exception as e:
         response_message += (f"\n`\n{e}\n`")
         return response_message
    
    response_message += "``" + completion.choices[0].message.content + "``"
    #if len(response_message) > 2000:
     #    return split_message(response_message)
    return response_message

def split_message(message: str):
    #doesnt work lol
    messages = []
    message_count = 1
    for message_part in message.split("\n"):
        if len(messages[-1]) + len(message_part) + 1 > 2000:
            messages.append(f"`\n{message_count}. {message}\n`")
            message_count += 1
        else:
            messages[-1] += message_part + "\n"
    return messages