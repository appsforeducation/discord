import discord
import json
import os

client = discord.Client()
welcome_channel_id = 572400234249060357
welcome_message_id = 0
roles = json.load(open('welcome.json', 'r'))["roles"]

@client.event
async def on_ready():
	global welcome_message_id

	print('☛ 'f'{client.user}'', at your service.')
	
	# Init 🏠-bienvenue channel
	welcome_channel = client.get_channel(welcome_channel_id)
	last_messages = await welcome_channel.history(limit=1).flatten()
	
	if not last_messages:
		print('☛ Let me serve a warm and welcoming message for you sir.')
		welcome_raw = open('welcome.json', 'r')
		welcome_json = json.load(welcome_raw)

		welcome_message = await welcome_channel.send(welcome_json["message"])
		for role in roles:
			await welcome_message.add_reaction(role["emoji"])

		print('☛ All done, sir.')
		welcome_message_id = welcome_message.id
	
	else:
		print('☛ Let me hold that message for you sir.')
		welcome_message_id = last_messages[0].id


@client.event
async def on_message(message):
	print('☛ Let me clean that mess, sir.')
	
	if message.author != client.user:
		await message.delete();


@client.event
async def on_raw_reaction_add(reaction, author):
	if author != client.user:
		if reaction.message.id == welcome_message_id:
			print('☛ I do care, sir.')
			
			matchs = list(filter(lambda e: e["emoji"] == reaction.emoji, roles))

			if not matchs:
				await reaction.remove(author)
				print('☛ I have just cleaned up some mess for you, sir.')
			else :
				role = discord.utils.get(author.guild.roles, name=matchs[0]["name"])
				await author.add_roles(role)


@client.event
async def on_raw_reaction_remove(reaction, author):
	if author != client.user:
		if reaction.message.id == welcome_message_id:
			print('☛ I do care, sir.')
			
			matchs = list(filter(lambda e: e["emoji"] == reaction.emoji, roles))

			role = discord.utils.get(author.guild.roles, name=matchs[0]["name"])
			await author.remove_roles(role)

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
