from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command
from discord.ext.commands import BadArgument
from aiohttp import request
import discord
from discord import Member, Embed
from discord.utils import get
from discord.ext.commands import command, cooldown
import urllib.request
from random import choice
from typing import Optional, Union
from hashlib import sha256 as encrypt
from ..db import db
import asyncio


def hash_code(self, input):
    if len(input) == 6:
        return encrypt((input.upper()).encode()).hexdigest()
    else:
        return None


client = discord.Client()


class reg(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="reg")
    async def register(self, ctx, code):

        code_hash = hash_code(self, code)
        value = db.record(
            'SELECT HashID FROM HALLGATO WHERE UserID=?', ctx.author.id)

        if value[0] == code_hash:
            await ctx.send('Ezzel a kóddal már regisztráltak!')
        else:
            db.register(code_hash, ctx.author.id)
            embed = Embed(title="Regisztrációd mentve!",
                          description="most már hozzáférsz a szerverhez!", color=6784696)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/728549208688296026/736656736383008868/DISCORD_BOT.png")
            embed.add_field(name="Felhasználói azonosítód:",
                            value=f"`{ctx.author.id}`", inline=False)
            embed.add_field(name="NEPTUN Kódod:",
                            value=f"`{code.upper()}`", inline=False)
            embed.add_field(name="Egyedi azonosítód:",
                            value=f"||`{code_hash.upper()}`||", inline=False)

            await ctx.send('Regisztrációd mentve!')
            await ctx.author.send(embed=embed)


    @ Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("reg")


def setup(bot):
    bot.add_cog(reg(bot))
