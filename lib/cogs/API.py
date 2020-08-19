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


class API(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="fact")
	@cooldown(3, 60, BucketType.guild)
	async def animal_fact(self, ctx, animal: str):
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour=ctx.author.colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("No facts are available for that animal.")

	@command(name='upscale', aliases=["2x", "ups"])
	@cooldown(3, 60, BucketType.guild)
	async def Superresolution(self, ctx, *, image: Optional[Union[Member, str]]):

		await ctx.trigger_typing()
		if image is None:
			if hasattr(ctx, 'attachments'):
				image_url = ctx.attachments[0].url
			else:
				image_url = ctx.author.avatar_url
		elif hasattr(image, 'avatar_url'):
			image_url = image.avatar_url
		elif '.png' or '.jpg' or '.webp' in image:
			image_url = image
		else:
			await ctx.send('Ez nem kép!') #if its not a picture

		async with request('POST', 'https://api.deepai.org/api/torch-srgan',
						   data={'image': f'{image_url}', },
						   headers={'api-key': 'b85db86a-5856-43ca-8440-c7e76d3e0e87'}) as response:
			if response.status == 200:
				data = await response.json()
				image_link = data['output_url']
			else:
				image_link = ("Hiba!") #if Api is not status=200 some kind of error
			await ctx.send(image_link)

	@ Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("API")


def setup(bot):
	bot.add_cog(API(bot))
