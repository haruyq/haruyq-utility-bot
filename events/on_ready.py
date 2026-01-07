from discord.ext import commands

from mod.logger import Logger
from views.ticket import TicketView
from views.verify import VerifyView

Log = Logger(__name__)

class On_Ready(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        bot_user = self.bot.user
        if bot_user is None:
            return
        self.bot.add_view(TicketView())
        self.bot.add_view(VerifyView())
        Log.info(f"Logged in as {bot_user} (ID: {bot_user.id})")

async def setup(bot: commands.Bot):
    await bot.add_cog(On_Ready(bot))