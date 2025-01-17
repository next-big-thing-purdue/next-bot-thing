import discord
from discord.ext import commands

from bot import bot
import config

class DenyModal(discord.ui.Modal):

	def __init__(self, user_id):
		super().__init__(title='Deny User')

		self.user_id = user_id
		self.add_item(discord.ui.InputText(label='Reason', placeholder='Reason required'))

	async def callback(self, interaction: discord.Interaction):
		guild = interaction.guild
		reason = self.children[0].value

		if interaction.message is None:
			print('[?!] Could not get verification message')
		else:
			msg = interaction.message
			for i, field in enumerate(msg.embeds[0].fields):
				if field.name == 'Status':
					msg.embeds[0].set_field_at(i, name='Status', value='Denied')
				if field.name == 'Verified By':
					msg.embeds[0].set_field_at(i, name='Denied By', value=f'{interaction.user.name} ({interaction.user.id})')
			msg.embeds[0].add_field(name='Reason', value=reason)
			msg.embeds[0].color = discord.Color.light_gray()
			await msg.edit(embeds=msg.embeds, view=None)

		await interaction.response.send_message('Verification Complete!', ephemeral=True)
		member = guild.get_member(self.user_id)

		if member is None:
			print('[!!] Could not message member for denial')
			return
		
		embed = discord.Embed(
			).add_field(
				name='Reason',
				value=reason
			).set_footer(
				text='Please fix these issues and then reapply. Feel free to contact a moderator for more info.'
			)
		embed.color = discord.Color.yellow()
		await member.send(
			content='You have been denied. This is not a ban and you can still reapply once these issues are fixed.',
			embed=embed
		)

class BanModal(discord.ui.Modal):

	def __init__(self, user_id):
		super().__init__(title='Ban User')

		self.user_id = user_id
		self.add_item(discord.ui.InputText(label='Reason', placeholder='Reason required'))

	async def callback(self, interaction: discord.Interaction):
		guild = interaction.guild
		reason = self.children[0].value

		if interaction.message is None:
			print('[?!] Could not get verification message')
		else:
			msg = interaction.message
			for i, field in enumerate(msg.embeds[0].fields):
				if field.name == 'Status':
					msg.embeds[0].set_field_at(i, name='Status', value='Banned')
				if field.name == 'Verified By':
					msg.embeds[0].set_field_at(i, name='Banned By', value=f'{interaction.user.name} ({interaction.user.id})')
			msg.embeds[0].add_field(name='Reason', value=reason)
			msg.embeds[0].color = discord.Color.red()
			await msg.edit(embeds=msg.embeds, view=None)

		await interaction.response.send_message('Verification Complete!', ephemeral=True)
		member = guild.get_member(self.user_id)

		if member is None:
			print('[!!] Could not message member for ban')
			return
		
		embed = discord.Embed(
			).add_field(
				name='Reason',
				value=reason
			).set_footer(
				text='If you think you were banned in error, please contact a moderator.'
			)
		embed.color = discord.Color.red()
		await member.send(
			content='You have been banned. This is likely because moderators believed you to be a bot. If you think this is an error, please contact a moderator',
			embed=embed
		)
		
		try:
			await member.ban(reason=f'Verification-Banned by {interaction.user.name} ({interaction.user.id}). Reason: {reason}')
		except:
			print('[?!] Could not verification-ban user')

class ResponseButtons(discord.ui.View):
	def __init__(self, user_id):
		super().__init__()
		self.user_id = user_id

	# TODO: This holds state and does not work when the bot is restarted. Should instead use message/button data
	@discord.ui.button(label='Accept', style=discord.ButtonStyle.green)
	async def button_accept(self, button: discord.ui.Button, interaction: discord.Interaction):
		guild = interaction.guild
		if guild is None:
			print('[?!] Accepted verification from invalid Guild')
			return

		role_general_member = guild.get_role(config.ROLE_GENERAL_MEMBER_ID)
		if role_general_member is None:
			print('[!!] Could not get general member role')
			return

		try:
			await guild.get_member(self.user_id).add_roles(role_general_member, reason='Verified by TODO')
		except:
			print('[!!] Could not add role to accepted verification')
			return
		
		if interaction.message is None:
			print('[?!] Could not get verification message')
		else:
			msg = interaction.message
			for i, field in enumerate(msg.embeds[0].fields):
				if field.name == 'Status':
					msg.embeds[0].set_field_at(i, name='Status', value='Verified')
				if field.name == 'Verified By':
					msg.embeds[0].set_field_at(i, name='Verified By', value=f'{interaction.user.name} ({interaction.user.id})')
			msg.embeds[0].color = discord.Color.green()
			await msg.edit(embeds=msg.embeds, view=None)

		await interaction.response.send_message('Verification Complete!', ephemeral=True)

	@discord.ui.button(label='Deny', style=discord.ButtonStyle.gray)
	async def button_deny(self, button: discord.ui.Button, interaction: discord.Interaction):
		guild = interaction.guild
		if guild is None:
			print('[?!] Denied verification from invalid Guild')
			return

		await interaction.response.send_modal(DenyModal(self.user_id))

	@discord.ui.button(label='Ban', style=discord.ButtonStyle.red)
	async def button_ban(self, button: discord.ui.Button, interaction: discord.Interaction):
		guild = interaction.guild
		if guild is None:
			print('[?!] Banned verification from invalid Guild')
			return

		await interaction.response.send_modal(BanModal(self.user_id))

async def send_request(ctx: discord.ApplicationContext | discord.Message) -> None:
	guild: discord.Guild | None = ctx.guild
	is_msg = isinstance(ctx, discord.Message)
	if guild is None:
		if is_msg:
			return
		await ctx.response.send_message('`verify` can only be ran in guilds', ephemeral=True)
		return
	
	if is_msg:
		channel_id = ctx.channel.id
	else:
		channel_id = ctx.channel_id
	if channel_id != config.CHANNEL_VERIFICATION_ID:
		if is_msg:
			return
		await ctx.response.send_message('`verify` cannot be ran in this channel', ephemeral=True)
		return

	channel_verification_review = guild.get_channel(config.CHANNEL_VERIFICATION_REVIEW_ID)
	if channel_verification_review is None:
		print('[!!] Verification review channel is None')
		if is_msg:
			return
		await ctx.respond.send_message('An error has occurred, please contact a moderator or bot developer', ephemeral=True)
		return


	if is_msg:
		user: discord.Member = ctx.author
	else:
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
	embed.color = discord.Color.yellow()

	if is_msg:
		embed.add_field(
			name='Message',
			value=ctx.content
		)

	try:
		await channel_verification_review.send(embed=embed, view=ResponseButtons(user.id))
	except Exception as e:
		print('[!!] Cannot send to verification review channel')
		if is_msg:
			raise e
		await ctx.response.send_message('An error has occurred, please contact a moderator or bot developer', ephemeral=True)
		raise e
	
	if is_msg:
		return
	await ctx.response.send_message('Verification request sent! Please sit tight and a moderator will give you access shortly.', ephemeral=True)

@bot.slash_command(name='verify')
async def verify(ctx: discord.ApplicationContext) -> None:
	await send_request(ctx)

@bot.listen()
async def on_message(message: discord.Message) -> None:
	if message.channel.id != config.CHANNEL_VERIFICATION_ID:
		return
	await send_request(message)
	await message.delete()