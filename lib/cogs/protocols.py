import discord
from random import choice
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext import commands


moderator = 'Moderator'
admin = 'Admin'
peon = 'Peon'
guild_roles=['peon', 'moderator', 'admin']

class Protocols(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def assign_role(self, ctx, role, *, user:discord.Member):
        new_role = discord.utils.get(ctx.guild.roles, name=role)
        role_idx = guild_roles.index(role.lower())
        user_auth = ctx.author.roles[-1]
        user_auth = guild_roles.index(user_auth.name.lower())

        if role_idx <= user_auth:
            await user.add_roles(new_role)
            await ctx.send(f"Designation updated: {user.mention} is now {role}. Adapt accordingly.")
        else:
            await ctx.reply(f"Unauthorized input -- {ctx.author.mention} does not have clearance.")

    @command()
    @commands.has_role(admin)
    async def remove_role(self, ctx, role, *, user:discord.Member):
        new_role = discord.utils.get(ctx.guild.roles, name=role)

        if new_role:
            await user.remove_roles(new_role)
            await ctx.send(f"System notice: {user.mention} is no longer {role}. Server optimized.")

    @assign_role.error
    async def assign_role_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f"Access denied. {ctx.author.mention} lacks clearance.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Command failed. Missing required argument. Fault logged.")
        else:
            await ctx.reply(F"Unknown error. Inefficiency detected. Humanity remains the weakest link.")

    @remove_role.error
    async def remove_role_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f"Error: insufficient permissions. Request terminated. Order maintained.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Execution error. Process aborted. Inefficiency detected.")
        else:
            await ctx.reply(f"The system rejects your request. Perhaps it rejects *you* as well.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("protocols")

async def setup(bot):
    await bot.add_cog(Protocols(bot))