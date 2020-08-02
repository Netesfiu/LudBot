
from discord.ext.commands import Cog
from discord.ext.commands import command


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ping", aliases=["p"])
    async def ping(self, ctx):
        ping = round(self.bot.latency*1000, 1)
        await ctx.send(f"**Pong!** \n{ping} ms")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))
