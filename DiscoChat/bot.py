import sys

import discord
import os
import openai
from dotenv import load_dotenv
from discord.ext import commands
import argparse
import atexit

from utils.chatter_box import ChatterBox

version = "0.0.1"

load_dotenv()  # load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")  # set OpenAI API key from .env file

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)  # create a Discord bot instance

try:
    discord_user_id = int(os.getenv("DISCORD_USER_ID"))
except ValueError:
    print("Unable to cast discord id properly. Verify value is setup properly")
    discord_user_id = "NotSet"

chatter = ChatterBox()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Application ID: {bot.application_id}")
    print(f"Chat agent: {chatter.chat_agent}")


@bot.command()
async def describe_chat_agent(ctx: commands.Context):
    await ctx.send(f"DiscoChat Agent is set as \"{chatter.chat_agent}\"")


@bot.command(hidden=True)
async def set_chat_agent(ctx: commands.Context, *, chat_agent_description):
    chatter.chat_agent(chat_agent_description)
    await ctx.send(f"Attempting to update agent\nAgent set to \"{chatter.chat_agent}\"")


@bot.command(hidden=True)
async def check_user(ctx: commands.Context):
    """
    Playing around with permissions and handling around guilds/roles
    """
    channel = ctx.channel.name

    if await bot.is_owner(ctx.author):
        await ctx.send(f'Hello Owner')
    elif discord_user_id == ctx.author.id:
        await ctx.send(f'Hello Developer!')
    elif permission_check(ctx.author.roles, ['Admin', 'Tester']):
        await ctx.send(f'Checking')
        user = discord.utils.get(bot.get_all_members(), id=ctx.author.id)
        print(f'User:{user.name} and channel: {channel}')
    else:
        await ctx.send("So sorry! this functionality is protected")


@bot.command()
async def chat(ctx: commands.Context, *, question):
    response = chatter.send_to_agent(question)
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def sassy(ctx: commands.Context, *, question):
    response = chatter.send_to_sassy(question)
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def ask(ctx: commands.Context, *, question):
    response = chatter.send(question)
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def artsy(ctx: commands.Context, *, question):
    response = chatter.send_to_artsy(question)
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def code(ctx: commands.Context, *, question: str):
    """
    This command takes a string that will be passed to AI and returned formatted as code

    :param ctx: discord's commands.Context object
    :param question: Message that will be sent to AI
    """
    response = chatter.request_code_snippet(question)
    await ctx.send("```\n" + response.choices[0].text + "\n```")


@bot.command()
async def about(ctx: commands.Context):
    await ctx.send("DiscoChat is a basic chatGPT relay.\n"
                   f"Version {version}\n"
                   f"Code uses model: {chatter.model}\n"
                   "usage: !help <cmd> or @DiscoChat help <cmd>")


def graceful_shutdown():
    """
    stub for some alerting on shutdowns
        TODO see about adding a sign-off for the bot to post
    """
    try:
        print("Shutting down gracefully...")
        # Perform any necessary cleanup operations here.
    except Exception as e:
        # Log any errors that occur during the shutdown process.
        print("Error while shutting down: %s" % e)
    finally:
        # Exit the program.
        sys.exit(0)


def permission_check(author_roles, expected_roles):
    for role in expected_roles:
        if not discord.utils.get(author_roles, name=role):
            return False
    return True


# TODO add discord async errors
def main(verbose):
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # connect to Discord using the bot token


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChatGPT Bot")
    parser.add_argument("-v", "--verbose", dest="verbose", help="adds extra print lines", action="store_true")
    args = parser.parse_args()

    atexit.register(graceful_shutdown)

    main(args.verbose)
