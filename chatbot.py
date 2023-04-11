import os
import discord
import openai
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True)
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# OpenAI API key
API = 'your_api_key'
# Discord bot token
TOKEN = 'your_discord_bot_token'

openai.api_key = API

@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guilds:')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(client.user.mention):
        prompt = message.content[4:].strip()
        print(f"Received prompt: {prompt}")  # Terminal log for prompt
        response = get_gpt_response(prompt)
        print(f"Generated response: {response}")  # Terminal log for response
        await message.channel.send(response)

    await client.process_commands(message)

def get_gpt_response(prompt):
    model_engine = "gpt-3.5-turbo"
    response_length = 300
    prompt = f"{prompt}\n\n{model_engine} response:"

    # List of personalities, create new ones by following the template
    andrew = "You are Andrew, a 4th year philosophy student."
    assistant = "You are helpful assistant."

    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ],
        max_tokens=response_length,
        n=1,
        stop=None,

        # Creativity of responses, between 0-1
        temperature=0.8,
    )

    return completion.choices[0].message['content'].strip()

client.run(TOKEN)