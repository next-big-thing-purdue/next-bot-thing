# **DO NOT SHARE BOT TOKEN**
# BOT_TOKEN = '...'
import config

from bot import bot
import discord
import rxn_roles
import divisions

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user}')

@bot.event
async def on_raw_reaction_add(ctx: discord.RawReactionActionEvent):
	if ctx.user_id == bot.user.id:
		return
	
	if ctx.channel_id == config.CHANNEL_ROLES_ID:
		await rxn_roles.on_raw_reaction_add(ctx)

@bot.event
async def on_raw_reaction_remove(ctx: discord.RawReactionActionEvent):
	if ctx.user_id == bot.user.id:
		return

	# This will have to change if other rxn-based functionality is added
	if ctx.channel_id == config.CHANNEL_ROLES_ID:
		await rxn_roles.on_raw_reaction_remove(ctx)

if __name__ == '__main__':
	bot.run(config.BOT_TOKEN)