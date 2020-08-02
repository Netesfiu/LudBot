import random
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed
from discord.ext.commands import Bot as BotBase

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
            self.owner = self.get_user(OWNER_IDS[0])

            print(f"LudBot by {OWNER_IDS} \nVer.: {self.VERSION}")     

            channel = self.get_channel(689263784769880109)
            await channel.send(f"LudBot by {self.owner}")
            
            #embed rész
            before = time.monotonic()
            embed = Embed(title=f"LudBot Ver.: {self.VERSION}", description=f"*{random.choice(RANDOMQUOTES)}*", url="https://github.com/Netesfiu/LudBot")
            
            image_url= "https://cdn.discordapp.com/attachments/728549208688296026/736656736383008868/DISCORD_BOT.png"

            embed.set_thumbnail(url=image_url)
            embed.set_image
            fields = [("ping(API):",f"{round(self.latency*1000)} ms", True),
                      ("ping(Self):",f"{(time.monotonic()-before)*1000} ms",True)]
        
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await channel.send(embed=embed)
        
        else:
            print("Újracsatlakozva!")

    async def on_message(self, message):
        pass

bot = Bot()

