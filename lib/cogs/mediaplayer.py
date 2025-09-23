import nextcord
from nextcord.ext import commands
import wavelink
import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext import commands

class MediaPlayer(Cog):
    def __init__(self, bot):
        self.bot = bot