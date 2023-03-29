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

try:
    discord_user_id = int(os.getenv("DISCORD_USER_ID"))
except ValueError:
    print("Unable to cast discord id properly. Verify value is setup properly")
    discord_user_id = "NotSet"

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
    if not permission_check(ctx.author.roles, ['Admin']):
        await ctx.send(f"So sorry! I can't do that see your admin for privileges")
    else:
        global chat_agent
        chat_agent = chat_agent_description
        await ctx.send(f"Attempting to update agent\nAgent set to \"{chat_agent}\"")


@bot.command()
async def check_user(ctx):
    channel = ctx.channel.name
    if discord_user_id == ctx.author.id:
        await ctx.send(f'Hello owner!')
    elif permission_check(ctx.author.roles, ['Admin', 'Tester']):
        await ctx.send(f'Checking')
        user = discord.utils.get(bot.get_all_members(), id=ctx.author.id)
        print(f'User:{user.name} and channel: {channel}')
    else:
        await ctx.send("So sorry! this functionality is protected")


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
async def artsy(ctx, *, question):
    response = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": "Generate midjourney prompts by supplying very specific, detailed words "
                                          "capable of relaying imagery to nearly everyone"},
            # {"role": "system", "content": "Respond as a full tenured art instructor who specializes in rembrandt and "
            #                               "picaso"},
            {"role": "user", "content": "imagine yourself as a world renown artist such as Rembrant, Picaso and Monet"
                                        "using a wide vocabulary to accurately depict their painting "
                                        "to an audience that can't see it "},
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
                   "`!describe_chat_agent` returns the currently set value for the chat agent's system message\n"
                   "`!set_chat_agent` updates chat agent's system message\n"
                   "`!ask` provides chat model answer with no system message\n"
                   "`!sassy` provides chat from a opinionated, spoiled teenage girl\n"
                   "`!chat` provides chat model answers with simple system message")


# TODO see about adding a sign-off for the bot to post
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


# Not fully flushed out, but feel like functionality will be useful across functions
# TODO think about design of this function, may be easier for called to just pass ctx
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
