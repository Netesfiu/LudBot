from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, File
from random import choice
from discord.ext.commands import Bot
from asyncio import sleep


class default(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ping", aliases=["p"])
    async def ping(self, ctx):
        await ctx.trigger_typing()

        ping = round(self.bot.latency*1000, 1)

        await ctx.send(f"**Pong!** \n{ping} ms")

    @command(name="info", aliases=["about"])
    async def embed_info(self, ctx):
        ping = round(self.bot.latency*1000, 1)
        embed = Embed(title=f"LudBot by {ctx.guild.owner}", description=f"*{choice(('Dont judge.. Ezt egy környezetmérnök írta','És emiatt aludtam átlag napi 3 órát','Milyen napot írunk?','Amugy semmi közöm a programozáshoz','Mi az a Szabadidő?','Mérnöknek lenni jó'))}*",
                      url="https://github.com/Netesfiu/LudBot", colour=6784696)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/728549208688296026/736656736383008868/DISCORD_BOT.png")
        fields = [("Ping:",f"{ping} ms", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name=ctx.guild.name,
                         icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @ Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("default")


def setup(bot):
    bot.add_cog(default(bot))
