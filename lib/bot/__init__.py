from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from ..db import db

PREFIX = "//"
OWNER_IDS = [173849172833730560]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" '{cog}' modul betöltve!")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"'{cog}' modul megtalálva!")

        print("ez minden amit találtam!")

    def run(self, version):
        self.VERSION = version

        print ("Inicializálás...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print ("Bot indítása...")
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
        raise err

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
            # await ctx.send("nincs ilyen parancs")

        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:

            self.guild = self.get_guild(671997532628451354)
            self.stdout = self.get_channel(689263784769880109)
            self.owner = self.get_user(OWNER_IDS[0])
            self.scheduler.start()

            print(f"LudBot by {self.owner} \nVer.: {self.VERSION}")

            await self.stdout.send(f"LudBot by {self.owner}")


            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Online!")
            self.ready = True
            print("A bot üzemkész!")

        else:
            print("Újracsatlakozva!")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
