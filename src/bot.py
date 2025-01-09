import discord
import config

intents = discord.Intents.default()
intents.reactions = True
intents.members = True

bot = discord.Bot(intents=intents, debug_guilds=[config.GUILD_IDS])