import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

colour_list = ["Red", "Yellow", "Green", "Purple", "Orange"]

landing_pad_channel_id = 974327554188144640
colour_channel_id = 974717469975515166
guild_id = 974327441323593748



def hextoint(s):
    return int("0x" + s, base=16)


def get_role(role_name):
    guild = discord.utils.get(bot.guilds, id=guild_id)
    role = discord.utils.get(guild.roles, name=role_name)
    return role


async def role_removal(member, role_name_list):
    roles = []
    for role_name in role_name_list:
        roles.append(get_role(role_name))
    await member.remove_roles(*roles)


async def role_addition(member, role_name):
    await member.add_roles(get_role(role_name))


async def role_remove_all_and_add(member, role_name):
    await role_removal(member, colour_list)
    await role_addition(member, role_name)


@bot.event
async def on_ready():
    print("Ready to run")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == landing_pad_channel_id:
        if payload.emoji.name == "✅":
            await payload.member.remove_roles(get_role("landing pad"))

    # 7614 is the colours channel
    if payload.channel_id == colour_channel_id:
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

        if payload.emoji.name == "1️⃣":
            await role_addition(payload.member, "Section 201")

        if payload.emoji.name == "2️⃣":
            await role_addition(payload.member, "Section 202")


@bot.event
async def on_member_join(member):
    await member.add_roles(get_role("landing pad"))


@bot.event
async def on_message(message):
    if message.channel.id == 974714336599769139:
        if message.content[:2] == "0x":
            red = hextoint(message.content[2:4])
            green = hextoint(message.content[4:6])
            blue = hextoint(message.content[6:8])
            colour = discord.Colour.from_rgb(red, green, blue)
            guild = discord.utils.get(bot.guilds, id=928749914207432745)
            role = await guild.create_role(name=message.content[2:8] + " (Course Staff)", colour=colour)
            await role.edit(position=len(guild.roles) - 2)
            roles_to_add = [role]
            await message.author.add_roles(*roles_to_add)

    # if message.content == "!office-hours":
    #     if message.channel.id == 932531585306202154:
    #         await message.channel.send(
    #             "https://canvas.ubc.ca/courses/83388/pages/schedule-tutorials-and-office-hours?module_item_id=3896064")

    if message.content == "!start":
        embedVar = discord.Embed(title="This is where you obtain colours", description="", color=0x123456)
        embedVar.add_field(name="Simply react using the colour you want and you will receive that colour",
                           value="\u200b",
                           inline=False)
        await message.channel.send(embed=embedVar)


# shout out to https://github.com/Person314159/cs221bot for how to hide the bot token
load_dotenv()
token = os.getenv("BOT_KEY")
bot.run(token)
