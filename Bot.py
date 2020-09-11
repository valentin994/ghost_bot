import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f'pong <@{ctx.author.id}>')


#   General moderation

@bot.command(name="kick", help="Kick user")
@commands.has_role("admin")
async def kick(ctx, target: discord.Member, reason=None):
    await target.kick(reason=reason)
    await ctx.send(f"There is no user by the name {target}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Could not find that user")


@bot.command(name="purge", help="Delete messages in the channel, if no number is specified 100 msgs will be deleted.")
@commands.has_role("admin")
async def purge(ctx, limit: int = 100):
    await ctx.channel.purge(limit=limit)


@bot.command(name="ban", help="Ban user")
@commands.has_role("admin")
async def ban(ctx, target: discord.Member, reason=None):
    if ctx.author.id:
        await ctx.send("You can't ban yourself")
        return
    await target.ban(reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Could not find that user")

#   Role Commands

@bot.command(name="add_role",
             help="First argument is the role name which is mandatory, second one is an optional colour if not provided is white.")
@commands.has_role("admin")
async def add_role(ctx, name=None, color="#000000"):
    if name is None:
        await ctx.send("Name was not specified")
        raise ValueError("Name was not provided")
    try:
        col = color.replace("#", "0x")
        col = int(col, 16)
        await ctx.guild.create_role(name=name, color=discord.Colour(col))
        await ctx.send(f"Create a role with the name: {name}, and color {color}")
    except ValueError:
        await ctx.send("Color code format bad.")


@bot.command(name="delete_role", help="Delete a role specified by name")
@commands.has_role("admin")
async def delete_role(ctx, role: discord.Role):
    if role is None:
        await ctx.send("Please specify a role name")
    try:
        await role.delete()
        await ctx.send(f'{role} has been deleted.')
    except discord.Forbidden:
        await ctx.send('Permission error')


@bot.command(name="assign_role", help="Assign yourself a role")
@commands.has_role("admin")
async def assign_role(ctx, role):
    try:
        role = discord.utils.get(ctx.guild.roles, name=role)
        await discord.Member.add_roles(ctx.author, role)
    except:
        await ctx.send("The role doesn't exist")


@bot.command(name="remove_role", help="Remove a role that you specify")
async def assign_role(ctx, role):
    try:
        role = discord.utils.get(ctx.guild.roles, name=role)
        await discord.Member.remove_roles(ctx.author, role)
    except:
        await ctx.send("The role doesn't exist")


@bot.command(name="roles", help="Show all available roles")
async def roles(ctx):
    roles = []
    for r in ctx.guild.roles:
        if r.name != "@everyone":
            roles.append(r.name)
    await ctx.send(roles)


bot.run(TOKEN)
