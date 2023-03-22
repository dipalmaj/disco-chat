import sys

import discord
import os
import openai
from dotenv import load_dotenv
from discord.ext import commands
import argparse
import atexit


load_dotenv()  # load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")  # set OpenAI API key from .env file

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)  # create a Discord bot instance

client = discord.Client(intents=intents)

model = "text-davinci-003"
chat_model = "gpt-3.5-turbo"
# model = "text-davinci-002"

# @client.event()
# async def on_ready():
#     print(f"Client Logged in with {client.user.name}")
#     print(f"Client AppId {client.application_id}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Application ID: {bot.application_id}")
    # commandTree = discord.app_commands.CommandTree(client)
    # await commandTree.sync()


@bot.command()
async def chat(ctx, *, question):
    response = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": "You are a helpful chat agent helping software developers with questions"},
            {"role": "user", "content": question}
        ]
    )
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def ask(ctx, *, question):
    response = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def code(ctx, *, question):
    # print(f"Received question: {question}")
    response = openai.Completion.create(
        model=model,
        prompt=question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    await ctx.send("```\n" + response.choices[0].text + "\n```")


@bot.hybrid_command()
async def about(ctx):
    await ctx.send("DiscoChat is a basic chatGPT relay.\n"
                   f"Code uses model: {model}\n"
                   "`!code` will respond using code block formatting\n"
                   f"Ask and Chat make use of chat model: {chat_model}\n"
                   "`!ask` provides chat model answer with no system message\n"
                   "`!chat` provides chat model answers with simple system message")


def graceful_shutdown():
    try:
        print("Shutting down gracefully...")
        # Perform any necessary cleanup operations here.
    except Exception as e:
        # Log any errors that occur during the shutdown process.
        print("Error while shutting down: %s" % e)
    finally:
        # Exit the program.
        sys.exit(0)


def main(verbose):
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # connect to Discord using the bot token


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChatGPT Bot")
    parser.add_argument("-v", "--verbose", dest="verbose", help="adds extra print lines", action="store_true")
    args = parser.parse_args()

    atexit.register(graceful_shutdown)

    main(args.verbose)
