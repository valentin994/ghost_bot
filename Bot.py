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


@bot.command(name="purge", help="Delete messages in the channel, if no number is specified 100 msgs will be deleted.")
@commands.has_role("admin")
async def purge(ctx, limit: int = 100):
    await ctx.channel.purge(limit=limit)


@bot.command(name="add_role",
             help="First argument is the role name which is mandatory, second one is an optional colour if not provided is white.")
@commands.has_role("admin")
async def edit_role(ctx, name, color="#FFFFFF"):
    if (name):
        try:
            col = color.replace("#", "0x")
            col = int(col, 16)
            await ctx.guild.create_role(name=name, color=discord.Colour(col))
            await ctx.send(f"Create a role with the name: {name}, and color {color}")
        except ValueError:
            await ctx.send("Wrong colour format, use hex code.")
    else:
        await ctx.send("No name was provided")


bot.run(TOKEN)
