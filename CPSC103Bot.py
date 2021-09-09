import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def get_landing_role():
    guild = discord.utils.get(bot.guilds, id=885385922361827358)
    landing_role = discord.utils.get(guild.roles, id=885387549948911656)
    return landing_role


@bot.event
async def on_ready():
    print("Ready to run")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 885386228625711115:
        if payload.emoji.name == "✅":
            await payload.member.remove_roles(get_landing_role())


@bot.event
async def on_member_join(member):
    await member.add_roles(get_landing_role())


# shout out to https://github.com/Person314159/cs221bot for how to hide the bot token
load_dotenv()
token = os.getenv("BOT_KEY")
bot.run(token)
