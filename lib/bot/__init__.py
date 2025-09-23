import discord
import asyncio
from asyncio import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.app_commands import CommandNotFound
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord import Embed
from ..db import db
from glob import glob
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "!"
OWNER_IDS =[352217688271224834]
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"    > {cog} cog loaded")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=intents)

    async def setup(self):
        for cog in COGS:
            await self.load_extension(f"lib.cogs.{cog}")

        print("Setup Complete")

    def run(self, version):
        self.VERSION = version

        print("Running setup...")
        asyncio.run(self.setup())

        print("Boot protocol...")
        super().run(DISCORD_TOKEN, reconnect=True)

    async def on_connect(self):
        print("Ultron has connected")

    async def on_disconnect(self):
        print("Ultron disconnecting")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Error has occurred.")
        else:
            await self.stdout.send("Error has occurred.")
        raise

    async def on_commmand_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(1417666028023844936)
            self.scheduler.start()

            self.stdout = self.get_channel(1417943465475444949)

            embed = Embed(title="Boot Protocol", description="Systems now at 100%")
            embed.set_author(name="Ultron", icon_url=self.user.avatar)
            await self.stdout.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("Systems ready...")
        else:
            print("I have reconnected")


    async def on_message(self, message):
        if message.author == bot.user:
            return

        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()