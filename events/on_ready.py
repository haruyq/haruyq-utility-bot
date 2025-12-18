from discord.ext import commands

from mod.logger import Logger

Log = Logger(__name__)

class On_Ready(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        Log.info(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")

async def setup(bot: commands.Bot):
    await bot.add_cog(On_Ready(bot))