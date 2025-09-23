import discord

from lib.bot import bot

VERSION = "0.0.5"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot.run(VERSION)