import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

colour_list = ["Red", "Yellow", "Green", "Purple", "Orange"]


def get_role(role_name):
    guild = discord.utils.get(bot.guilds, id=885385922361827358)
    role = discord.utils.get(guild.roles, name=role_name)
    return role


async def role_removal(member, role_name_list):
    roles = []
    for role_name in role_name_list:
        print("Role added to list successfully")
        roles.append(get_role(role_name))
    await member.remove_roles(*roles)


async def role_addition(member, role_name):
    get_role(get_role(role_name))
    await member.add_roles()


async def role_remove_all_and_add(member, role_name):
    await role_removal(member, colour_list)
    print("roles removed")
    await role_addition(member, role_name)
    print("roles added")


@bot.event
async def on_ready():
    print("Ready to run")


@bot.event
async def on_raw_reaction_add(payload):
    # 1115 is the landing_pad channel
    if payload.channel_id == 885386228625711115:
        if payload.emoji.name == "✅":
            await payload.member.remove_roles(get_role("landing pad"))

    # 7614 is the colours channel
    if payload.channel_id == 885539737291587614:
        # this is a red square
        if payload.emoji.name == "🟥":
            await role_remove_all_and_add(payload.member, "Red")

        # this is a purple square
        if payload.emoji.name == "🟪":
            await role_remove_all_and_add(payload.member, "Purple")

        # this is a yellow square
        if payload.emoji.name == "🟨":
            await role_remove_all_and_add(payload.member, "Yellow")

        # this is a orange square
        if payload.emoji.name == "🟧":
            await role_remove_all_and_add(payload.member, "Orange")

        # this is a green square
        if payload.emoji.name == "🟩":
            await role_remove_all_and_add(payload.member, "Green")

        if payload.emoji.name == "❌":
            await role_removal(payload.member, colour_list)


@bot.event
async def on_member_join(member):
    await member.add_roles(get_role("landing pad"))


# shout out to https://github.com/Person314159/cs221bot for how to hide the bot token
load_dotenv()
token = os.getenv("BOT_KEY")
bot.run(token)
