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

@bot.command(name="add_role")
@commands.has_role("admin")
async def edit_role(ctx):
    await ctx.guild.create_role(name="abc")



bot.run(TOKEN)
