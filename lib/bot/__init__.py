from asyncio import sleep
from datetime import datetime
from glob import glob
import sys
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
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot, message):
    prefix = db.field(
        "SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


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
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"'{cog}' modul megtalálva!")

        print("ez minden amit találtam!")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))

        db.multiexec("INSERT OR IGNORE INTO HALLGATO (UserID) VALUES (?)",
                     ((member.id,) for member in self.guild.members if not member.bot))

        for member in self.guild.members:
            if not member.bot and db.field("SELECT HashID FROM HALLGATO WHERE UserID=?", member.id) == 'NONE':
                member_roles = ",".join([str(r.id) for r in member.roles])
                db.execute("UPDATE HALLGATO SET Roles=? WHERE UserID=?",member_roles, member.id)

        to_remove = []
        stored_members = db.column("SELECT UserID FROM HALLGATO")
        for id_ in stored_members:
            if not self.guild.get_member(id_):
                to_remove.append(id_)

        db.multiexec("DELETE FROM HALLGATO WHERE UserID = ?",
                     ((id_,) for id_ in to_remove))

        db.commit()

    def run(self, version):
        self.VERSION = version

        print("Inicializálás...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Bot indítása...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("Nemtudok fogadni több parancsot! Kérlek várj pár másodpercet")

    async def rules_reminder(self):
        await self.stdout.send("Remember to adhere to the rules!")

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
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Egy, vagy több argumentum hiányzik!")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Ez a parancs {str(exc.cooldown.type).split('.')[-1]} időnként használható. Próbált úrja {exc.retry_after:,.2f} mp múlva.")

        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
            # 	await ctx.send("Unable to send message.")

            if isinstance(exc.original, Forbidden):
                await ctx.send("Nincs jogom ehhez a művelethez!")

            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:

            self.guild = self.get_guild(671997532628451354)
            self.stdout = self.get_channel(689263784769880109)
            self.owner = self.get_user(OWNER_IDS[0])
            self.scheduler.add_job(self.rules_reminder, CronTrigger(
                day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            self.update_db()

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
