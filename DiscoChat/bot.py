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

chat_agent = "You are a helpful chat agent helping software developers with questions"


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Application ID: {bot.application_id}")
    print(f"Chat agent: {chat_agent}")


@bot.command()
async def describe_chat_agent(ctx):
    print(chat_agent)
    await ctx.send(f"DiscoChat Agent is set as \"{chat_agent}\"")


@bot.command()
async def set_chat_agent(ctx, *, chat_agent_description):
    global chat_agent
    chat_agent = chat_agent_description
    await ctx.send(f"Attempting to update agent\nAgent set to \"{chat_agent}\"")


@bot.command()
async def chat(ctx, *, question):
    response = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": chat_agent},
            {"role": "user", "content": question}
        ]
    )
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def sassy(ctx, *, question):
    response = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": "Respond as if you're a sassy teenage girl from Los Angeles. You've never "
                                          "worked a day in your life and have everything you want brought to you by a "
                                          "full staff"},
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


# Attempted to make use of hybrid_command which should allow commands to be registered to slash;
# however, you need to sync the CommandTree and that requires client...
# Didn't get it to work... discord.app_commands.CommandTree(client).sync()
@bot.hybrid_command()
async def about(ctx):
    await ctx.send("DiscoChat is a basic chatGPT relay.\n"
                   f"Code uses model: {model}\n"
                   "`!code` will respond using code block formatting\n"
                   f"Ask and Chat make use of chat model: {chat_model}\n"
                   "`!ask` provides chat model answer with no system message\n"
                   "`!sassy` provides chat from a opinionated, spoiled teenage girl\n"
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
