import discord
from discord.ext import commands

from bot import bot
import config

divisions_commands = bot.create_group('division', 'Division related commands')

@divisions_commands.command(name='new')
@discord.option('division_name', type=discord.SlashCommandOptionType.string)
@discord.option('division_abbr', type=discord.SlashCommandOptionType.string, required=False, default='')
@commands.has_permissions(manage_messages=True)
async def divisions_new(
	ctx: discord.ApplicationContext,
	division_name: str,
	division_abbr: str,
):
	guild: discord.Guild | None = ctx.guild
	if guild is None:
		await ctx.response.send_message(f'`division new` can only be ran in guilds', ephemeral=True)
		return
	
	if not division_abbr:
		division_abbr = division_name

	try:
		category = await guild.create_category(division_name)
	except discord.HTTPException:
		await ctx.response.send_message(f'invalid division name', ephemeral=True)
		return

	await category.set_permissions(
		guild.default_role, # @everyone
		overwrite=discord.PermissionOverwrite(view_channel=False),
	)

	await category.set_permissions(
		guild.get_role(config.ROLE_GENERAL_MEMBER_ID),
		overwrite=discord.PermissionOverwrite(view_channel=True),
	)

	await category.set_permissions(
		guild.get_role(config.ROLE_ACTIVE_MEMBER_ID),
		overwrite=discord.PermissionOverwrite(view_channel=True),
	)

	await category.create_text_channel(f'{division_abbr}-announcements')
	await category.create_text_channel(f'{division_abbr}-general')
	await ctx.response.send_message(f'division created successfully', ephemeral=True)