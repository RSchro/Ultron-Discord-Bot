import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "!"
OWNER_IDS =[352217688271224834]
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=intents)

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Boot protocol...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Ultron has connected")

    async def on_disconnect(self):
        print("Ultron disconnecting")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(1417666028023844936)
            print("Ultron systems ready...")

        else:
            print("I have reconnected")


    async def on_message(self, message):
        pass

bot = Bot()