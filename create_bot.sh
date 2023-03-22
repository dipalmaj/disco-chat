#!/bin/bash

echo "Welcome to the Discord bot setup script!"
echo ""

# Get the name of the bot
read -p "Enter a name for your bot: " bot_name

# Create a new directory for the project
mkdir $bot_name
cd $bot_name

# Create a virtual environment for the project
python3 -m venv env
source env/bin/activate

# Install the required dependencies
pip install discord.py python-dotenv openai

# Prompt for OpenAI API key
echo "You will now need to provide your OpenAI API key."
echo "You can find your API key in the OpenAI dashboard."
echo ""
read -p "Enter your OpenAI API key: " openai_api_key

# Prompt for Discord bot token
echo ""
echo "You will now need to create a Discord bot and obtain its token."
echo "You can follow the instructions here: https://discord.com/developers/docs/intro"
echo ""
read -p "Enter your Discord bot token: " discord_bot_token

# Create the .env file
touch .env
echo "OPENAI_API_KEY=$openai_api_key" >> .env
echo "DISCORD_BOT_TOKEN=$discord_bot_token" >> .env

# Create the Python script
echo ""
echo "Creating the Python script..."
cat <<EOT >> bot.py
import discord
import os
import openai
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")  # set OpenAI API key from .env file

client = discord.Client()  # create a Discord client instance


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = openai.Completion.create(
        engine="davinci",
        prompt=message.content,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    await message.channel.send(response.choices[0].text)


client.run(os.getenv("DISCORD_BOT_TOKEN"))  # connect to Discord using the bot token
EOT

# How to start the bot
echo "Perform the following commands to run the bot"
echo "source env/bin/activate"
echo "python bot.py"

