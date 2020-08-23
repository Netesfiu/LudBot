from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command
from discord.ext.commands import BadArgument
from aiohttp import request
import discord
from discord import Member, Embed
from discord.ext.commands import command, cooldown
import urllib.request
from random import choice
from typing import Optional, Union
from hashlib import sha256 as encrypt

from ..db import db


class reg(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="reg")
	async def register(self, ctx, code):

		def hash_code(self, input):
			if len(input) == 6:
				return encrypt((input.upper()).encode()).hexdigest()
			else:
				return None
		
		code = hash_code(self, code)
		value = db.record('SELECT HashID FROM HALLGATO WHERE UserID=?', ctx.author.id)

		if value == code:
			await ctx.send('Ezzel a kóddal már regisztráltak!')
		else:
			db.execute('UPDATE HALLGATO SET HashID=? WHERE UserID=?', code, ctx.author.id)
			await ctx.send(f'Regisztrációd mentve! `{code}` `{ctx.author.id}` `{value}`')

	@ Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("reg")


def setup(bot):
	bot.add_cog(reg(bot))
