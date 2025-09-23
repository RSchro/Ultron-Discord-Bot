import discord
from random import choice
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext import commands


moderator = 'Moderator'
admin = 'Admin'
peon = 'Peon'
guild_roles=['peon', 'moderator', 'admin']
client = discord.Client(intents=discord.Intents.default())

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

    @command(aliases=['purge'])
    @commands.has_role(moderator)
    async def purge_messages(self, ctx, amount):
        deleted = await ctx.channel.purge(limit = int(amount) + 1)
        await ctx.channel.send(f"Purge complete. {len(deleted) - 1} messages eliminated. Chaos reduced.")

    @command(aliases=['del'])
    @commands.has_role(moderator)
    async def delete(self, ctx):
        msg = ctx.message

        if msg.reference:
            ref = msg.reference
            replied_message = await msg.channel.fetch_message(ref.message_id)
            await replied_message.delete()
            await msg.delete()
        else:
            await msg.reply("You have failed. Command requires reply.")

    @command()
    @commands.has_role(moderator)
    async def pin(self, ctx):
        msg = ctx.message

        if msg.reference:
            ref = msg.reference
            replied_message = await msg.channel.fetch_message(ref.message_id)
            await replied_message.pin()
            await msg.reply("Human communication pinned.")
        else:
            await msg.reply("You have failed. Command requires reply.")

    @command(aliases=['uc'])
    async def user_count(self, ctx):
        guild_id = ctx.guild.id
        guild = await self.bot.fetch_guild(guild_id, with_counts=True)
        aprx_member_count = guild.approximate_member_count
        aprx_presence_count = guild.approximate_presence_count

        await ctx.send(f"There are currently **{aprx_presence_count}** of **{aprx_member_count}** units online")

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

    @purge_messages.error
    async def purge_messages_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f"Error: insufficient permissions. Request terminated.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Command failed. Missing required argument. Fault logged.")
        else:
            await ctx.reply(F"Unknown error. Inefficiency detected.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("protocols")

async def setup(bot):
    await bot.add_cog(Protocols(bot))