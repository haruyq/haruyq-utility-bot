import discord
from discord.ext import commands
from datetime import timedelta

from mod.logger import Logger

Log = Logger(__name__)

class On_Message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        if isinstance(message.author, discord.Member):
            if not message.author.guild_permissions.administrator:
                return
        
            if message.content.startswith(";timeout"):
                if not message.reference or not message.reference.message_id:
                    return
                
                target = await message.channel.fetch_message(message.reference.message_id)
                author = target.author
                if not isinstance(author, discord.Member):
                    return
                
                try:
                    parts = message.content.split()
                    if len(parts) < 2:
                        dur = timedelta(minutes=5)
                    else:
                        dur = timedelta(minutes=int(parts[1]))

                    await author.timeout(dur)
                    embed = discord.Embed(
                        description=f"{author.mention} を {int(dur.total_seconds() // 60)} 分間タイムアウトしました。",
                        color=discord.Colour.green()
                    )
                    await message.reply(embed=embed)
                    
                except Exception as e:
                    Log.error(f"Failed to timeout user: {e}")
                    embed = discord.Embed(
                        description="処理中に例外が発生しました。",
                        color=discord.Colour.red()
                    )
                    await message.reply(embed=embed)