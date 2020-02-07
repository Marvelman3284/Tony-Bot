import discord
import time
import asyncio
import json
import os
from discord.ext import commands


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()
client = commands.bot(commands_prefix = "!")

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
#CODE

	await update_data(users, message.author)
	await add_experiance(users, message.author, 5)
	await level_up(users, message.author, message.channel)

	with open('users.json', "w") as f:
		json.dump(users, f)

async def update_data(users, user):
	if not user.id in users:
		users[user.id] = {}
		users[user.id]['experiance'] = 0
		users[user.id]['level'] = 1

async def add_experiance(users, user, exp):
	users[user.id]['experiance'] += exp

async def level_up(users, user, channel):
	experiance = users[user.id]['experiance']
	lvl_start = users[user.id]['level']
	lvl_end = int(experiance ** (1/4))

	if lvl_start < lvl_end:
		await client.send_message(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
		users[user.id]['level'] = lvl_end

client.run(read_token)