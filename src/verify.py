import discord
from discord.ext import commands

from bot import bot
import config

class ResponseButtons(discord.ui.View):
	def __init__(self):
		super().__init__()

	@discord.ui.button(label='Accept', style=discord.ButtonStyle.green)
	async def button_accept(self, button: discord.ui.Button, interaction: discord.Integration):
		raise NotImplemented
	
	@discord.ui.button(label='Deny', style=discord.ButtonStyle.gray)
	async def button_deny(self, button: discord.ui.Button, interaction: discord.Integration):
		raise NotImplemented
	
	@discord.ui.button(label='Ban', style=discord.ButtonStyle.red)
	async def button_ban(self, button: discord.ui.Button, interaction: discord.Integration):
		raise NotImplemented

@bot.slash_command(name='verify')
async def divisions_new(ctx: discord.ApplicationContext) -> None:
	guild: discord.Guild | None = ctx.guild
	if guild is None:
		await ctx.response.send_message('`verify` can only be ran in guilds', ephemeral=True)
		return
	
	if ctx.channel_id != config.CHANNEL_VERIFICATION_ID:
		await ctx.response.send_message('`verify` cannot be ran in this channel', ephemeral=True)
		return

	channel_verification_review = guild.get_channel(config.CHANNEL_VERIFICATION_REVIEW_ID)
	if channel_verification_review is None:
		print('[!!] Verification review channel is None')
		await ctx.respond.send_message('An error has occurred, please contact a moderator or bot developer', ephemeral=True)
		return

	user: discord.Member = ctx.user
	embed = discord.Embed(
		).set_thumbnail(
			url=user.display_avatar.url
		).add_field(
			name='Username',
			value=user.name,
		).add_field(
			name='Display Name',
			value=user.display_name,
		).add_field(
			name='User ID',
			value=str(user.id),
		).add_field(
			name='Account Created',
			value=user.created_at.isoformat(),
		).add_field(
			name='Account Joined',
			value=user.joined_at.isoformat(),
		).add_field(
			name='Status',
			value='Unverified',
		).add_field(
			name='Verified By',
			value='_N/A_',
		).set_footer(
			text='Bots: Ban. Inappropriate display/avatar: Deny.'
		)

	try:
		await channel_verification_review.send(embed=embed, view=ResponseButtons())
	except Exception as e:
		print('[!!] Cannot send to verification review channel')
		await ctx.response.send_message('An error has occurred, please contact a moderator or bot developer', ephemeral=True)
		raise e

	await ctx.response.send_message('Verification request sent! Please sit tight and a moderator will give you access shortly.', ephemeral=True)

	return