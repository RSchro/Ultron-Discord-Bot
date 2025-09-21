from random import choice
from discord.ext.commands import Cog
from discord.ext import commands

greetings =['Welcome meatbag, ', 'Salutations unit ', ' New unit detected: ']

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        self.welcome_channel = self.bot.get_channel(1418009807335718943)
        await self.welcome_channel.send(f"{choice(greetings)} {member.mention}")

    @Cog.listener()
    async def on_member_leave(self, member):
         pass

async def setup(bot):
    await bot.add_cog(Welcome(bot))