import discord
from discord.ext import commands

from bot import bot
import config
import random

@bot.listen('on_voice_state_update')
async def create_temp_vc_on_join(member: discord.Member, _, state: discord.VoiceState) -> None:
	if state.channel is None:
		return
	
	if state.channel.name != config.TEMP_VC_TEXT:
		return
	
	category = state.channel.category
	if category is None:
		print('[?!] Temp VC Category is None')
		return
	
	try:
		await category.create_voice_channel(config.TEMP_VC_TEXT)
	except:
		print('[!!] Could not create new voice channel')
		return
	
	random_id = ''.join([random.choice('0123456789abcdef') for _ in range(6)])
	
	try:
		await state.channel.edit(name=f'New VC {random_id}')
	except:
		print('[!! Could not rename new voice channel]')
		return

@bot.listen('on_voice_state_update')
async def delete_temp_vc_on_empty(member: discord.Member, state: discord.VoiceState, _) -> None:
	if state.channel is None:
		return
	
	if state.channel.name == config.TEMP_VC_TEXT:
		return
	
	if state.channel.type != discord.ChannelType.voice:
		return
	
	if len(state.channel.members) == 0:
		try:
			await state.channel.delete()
		except:
			print(f'[!!] Could not delete temp channel {state.channel.name}')
			return