from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "//"
OWNER_IDS = [173849172833730560]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

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

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(671997532628451354)

            print(f"LudBot by {OWNER_IDS} \nVer.: {self.VERSION}")     

            channel = self.get_channel(689263784769880109)
            await channel.send(f"LudBot by <@{OWNER_IDS[0]}> \nVer.: {self.VERSION}")

        else:
            print("Újracsatlakozva!")

    async def on_message(self, message):
        pass

bot = Bot()

