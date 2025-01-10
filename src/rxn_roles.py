import discord
from discord.ext import commands
import config
import re

from bot import bot

rxn_role_commands = bot.create_group('rxn-role', 'Reaction-role related commands')
rxn_role_add_commands = rxn_role_commands.create_subgroup('add')

@rxn_role_add_commands.command(name='section')
@discord.option('section_name', type=discord.SlashCommandOptionType.string)
@commands.has_permissions(manage_messages=True)
async def add_section(
	ctx: discord.ApplicationContext,
	section_name: str,
):
	if ctx.channel_id != config.CHANNEL_ROLES_ID:
		await ctx.response.send_message(f'rxn-role commands can only be ran in <#{config.CHANNEL_ROLES_ID}>', ephemeral=True)
		return

	await ctx.channel.send(f'# {section_name}')
	await ctx.response.send_message('Section created successfully', ephemeral=True)

@rxn_role_add_commands.command(name='role')
@discord.option('section_id', type=discord.Message) # Must be a string converted to int due to API restrictions
@discord.option('rxn_emoji', type=discord.SlashCommandOptionType.string)
@discord.option('rxn_role', type=discord.SlashCommandOptionType.role)
@discord.option('role_description', type=discord.SlashCommandOptionType.string, required=False, default='')
async def add_role(
	ctx: discord.ApplicationContext,
	section_id: discord.Message,
	rxn_emoji: str,
	rxn_role: discord.Role,
	role_description: str,
):
	if ctx.channel_id != config.CHANNEL_ROLES_ID:
		await ctx.response.send_message(f'rxn-role commands can only be ran in <#{config.CHANNEL_ROLES_ID}>', ephemeral=True)
		return

	# section_msg = bot.get_message(section_id)
	if section_id is None:
		await ctx.response.send_message(f'Section ID not found', ephemeral=True)
		return

	if section_id.author.id != bot.user.id: 
		await ctx.respond.send_message(f'Message not created by bot (sections must be created through /rxn-role add section ...)', ephemeral=True)
		return
	
	try:
		await section_id.add_reaction(rxn_emoji)
	except (discord.HTTPException, discord.NotFound):
		await ctx.response.send_message(f'Invalid emoji', ephemeral=True)
		return

	new_content = f'{section_id.content}\n{rxn_emoji} <@&{rxn_role.id}>'
	if role_description:
		new_content = f'{new_content} - {role_description}'

	await section_id.edit(content=new_content)

	await ctx.response.send_message(f'Role added successfully', ephemeral=True)

@bot.listen('on_raw_reaction_add')
async def give_role_on_reaction_add(ctx: discord.RawReactionActionEvent):
	if ctx.user_id == bot.user.id:
		return

	# This will have to change if other rxn-based functionality is added
	if ctx.channel_id != config.CHANNEL_ROLES_ID:
		return

	channel = await bot.fetch_channel(ctx.channel_id)

	if channel is None:
		print('[!!] #roles is None')
		return
 
	message = await channel.fetch_message(ctx.message_id)

	if message is None:
		print('[?!] User reacted to invalid message')
		return

	if message.author != bot.user:
		return
	
	lines = message.content.splitlines()
	prog = None

	if ctx.emoji.is_custom_emoji():
		prog = re.compile(r'<:.+?:([0-9]+?)> (<@&[0-9]+?>)')
	else:
		prog = re.compile(r'(.+?) (<@&[0-9]+?>)')

	for line in lines:
		match = prog.match(line)

		if match is None: continue

		emoji = match.group(1)
		role = match.group(2)

		try:
			emoji_id = int(emoji)
		except ValueError:
			pass

		if ctx.emoji.is_custom_emoji() and emoji_id != ctx.emoji.id:
			print(f'{emoji} is not {ctx.emoji.id}')
			continue
	
		if not ctx.emoji.is_custom_emoji() and emoji != ctx.emoji.name:
			continue

		guild = bot.get_guild(ctx.guild_id)
		role = guild.get_role(int(role.lstrip('<@&').rstrip('>')))
		await ctx.member.add_roles(role)

@bot.listen('on_raw_reaction_remove')
async def remove_role_on_reaction_removed(ctx: discord.RawReactionActionEvent):
	channel = await bot.fetch_channel(ctx.channel_id)

	if channel is None:
		print('[!!] #roles is None')
		return
 
	message = await channel.fetch_message(ctx.message_id)

	if message is None:
		print('[?!] User reacted to invalid message')
		return

	if message.author != bot.user:
		return
	
	lines = message.content.splitlines()
	prog = None

	if ctx.emoji.is_custom_emoji():
		prog = re.compile(r'<:.+?:([0-9]+?)> (<@&[0-9]+?>)')
	else:
		prog = re.compile(r'(.+?) (<@&[0-9]+?>)')

	for line in lines:
		match = prog.match(line)

		if match is None: continue

		emoji = match.group(1)
		role = match.group(2)

		try:
			emoji_id = int(emoji)
		except ValueError:
			pass

		if ctx.emoji.is_custom_emoji() and emoji_id != ctx.emoji.id:
			print(f'{emoji} is not {ctx.emoji.id}')
			continue
	
		if not ctx.emoji.is_custom_emoji() and emoji != ctx.emoji.name:
			continue

		guild = bot.get_guild(ctx.guild_id)
		role = guild.get_role(int(role.lstrip('<@&').rstrip('>')))
		member = guild.get_member(ctx.user_id)

		await member.remove_roles(role)