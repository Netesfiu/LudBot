import random
import time
from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
                                  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db


PREFIX = "//"
OWNER_IDS = [173849172833730560]
RANDOMQUOTES = [
    "Dont judge.. Ezt egy környezetmérnök írta",
    "És emiatt aludtam átlag napi 3 órát",
    "Milyen napot írunk?",
    "Amugy semmi közöm a programozáshoz",
    "Mi az a Szabadidő?",
    "Mérnöknek lenni jó"
]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Inicializálás...")
        super().run(self.TOKEN, reconnect=True)
       
    async def on_connect(self):
        print("Bot csatlakoztatva!")

    async def on_disconnect(self):
        print("Lecsatlakoztatva!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Valami félrement...")

        channel = self.get_channel(7395579881210513489)
        await channel.send("Hiba történt")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
            # await ctx.send("nincs ilyen parancs")

        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(671997532628451354)
            self.owner = self.get_user(OWNER_IDS[0])
            self.scheduler.start()

            print(f"LudBot by {self.owner} \nVer.: {self.VERSION}")

            channel = self.get_channel(689263784769880109)
            await channel.send(f"LudBot by {self.owner}")

            # embed rész
            # before = time.monotonic()
            # embed = Embed(title=f"LudBot Ver.: {self.VERSION}", description=f"*{random.choice(RANDOMQUOTES)}*",
            #               url="https://github.com/Netesfiu/LudBot", colour=6784696)

            # embed.set_thumbnail(url=self.user.avatar_url)

            # fields = [("ping(API):", f"{round(self.latency*1000)} ms", True),
            #              ("ping(Self):", f"{(time.monotonic()-before)*1000} ms", True)]

            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name=self.guild.name,
            # icon_url=self.guild.icon_url)
            # await channel.send(embed=embed)

        else:
            print("Újracsatlakozva!")

    async def on_message(self, message):
        pass


bot = Bot()
