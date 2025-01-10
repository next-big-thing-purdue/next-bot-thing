# **DO NOT SHARE BOT TOKEN**
# BOT_TOKEN = '...'
import config

from bot import bot

# The only side-effect these modules should have is registering functions with bot
import divisions
import rxn_roles
import temp_vc

@bot.listen
async def on_ready() -> None:
	print(f'Logged in as {bot.user}')

if __name__ == '__main__':
	bot.run(config.BOT_TOKEN)