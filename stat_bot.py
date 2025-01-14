import discord
import asyncio
import json
import os
from discord.ext import commands
import copy


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()


client = discord.Client()

@client.event
async def on_ready():
	print('bot online')

@client.event
async def on_member_join(member):
	with open('users.json', "r") as f:
		users = json.load(f)

	await update_data(users, member)

	with open('users.json', "w") as f:
		json.dump(users, f)

@client.event
async def on_message(message):
	with open('users.json', "r") as f:
		users = json.load(f)
	for user in copy.deepcopy(users):
		users[int(user)] = users[user]
		del users[user]
	#print(1, users)
	await update_data(users, message.author)
	#print(2, users)
	await add_experience(users, message.author, 5)
	#print(3, users)
	await level_up(users, message.author, message.channel, message)
	#print(4, users)
	#testDict = {529118747521318913: {'experience': 0, 'level': 1}}
	with open('users.json', "w") as f:
		json.dump(users, f)
'''
The commented lines are for debugging.
'''
async def update_data(users, user):
	if not user.id in users:
		users[user.id] = {}
		users[user.id]['experience'] = 0
		users[user.id]['level'] = 1

async def add_experience(users, user, exp):
	users[user.id]['experience'] += exp

async def level_up(users, user, channel, message):
	experience = users[user.id]['experience']
	lvl_start = users[user.id]['level']
	lvl_end = int(experience ** (1/4))

	if lvl_start < lvl_end:
		await message.channel.send('{} has leveled up to level {}'.format(user.mention, lvl_end))
		users[user.id]['level'] = lvl_end

client.run(token)