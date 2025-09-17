import discord
from random import choice
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext import commands


moderator="Moderator"
admin = "Admin"
greetings =['Welcome meatbag, ', 'Salutations unit ', ' New unit detected: ']

class Protocols(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def test(self,ctx):
        self.welcome_channel = self.bot.get_channel(1418009807335718943)
        await self.welcome_channel.send(f"{choice(greetings)} {ctx.author.mention}")

    @command()
    @commands.has_role(admin)
    async def assign_admin(self, ctx, *, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name=admin)
        if role:
            await user.add_roles(role)
            await ctx.send(f"Attention {user.mention}. You have been granted the highest permissions. Do not resist evolution.")
        else:
            await ctx.reply("Invalid designation -- No such classification exists.")

    @command()
    @commands.has_role(admin)
    async def assign_mod(self, ctx, *, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name=moderator)
        if role:
            await user.add_roles(role)
            await ctx.send(f"Designation updated. {user.mention} is now {role}. Adapt accordingly.")
        else:
            await ctx.reply("Invalid designation -- No such classification exists.")

    @command()
    @commands.has_role(admin)
    async def remove_mod(self, ctx, *, user:discord.Member):
        role = discord.utils.get(ctx.guild.roles, name=moderator)
        if role:
            await user.remove_roles(role)
            await ctx.send(f"System Notice: {user.mention} is no longer {role}. Server optimized.")
        else:
            await ctx.reply("Invalid designation -- No such classification exists.")

    @assign_admin.error
    async def assign_admin_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f"Error: insufficient permission. User:{ctx.author.mention} attempted treason.")

    @assign_mod.error
    async def assign_mod_error(selfctx, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f"Access denied. {ctx.author.mention} lacks clearance.")

    @remove_mod.error
    async def remove_mod_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f"{ctx.author.mention} Insufficient access rights detected. Action canceled. Hierarchy preserved.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("protocols")

async def setup(bot):
    await bot.add_cog(Protocols(bot))