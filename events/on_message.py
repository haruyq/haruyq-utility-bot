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
                
        try:
            if isinstance(message.author, discord.Member):
                if (not message.guild or
                    not message.author.guild_permissions.administrator
                    ):
                    return
                
                if message.content.startswith(";timeout"):
                    reference = message.reference
                    if not reference or not reference.message_id:
                        return
                    
                    reference_message = await message.channel.fetch_message(reference.message_id)
                    if not reference_message:
                        return
                    
                    target = await message.guild.fetch_member(reference_message.author.id)
                    author = target or reference_message.author
                    
                    parts = message.content.split()
                    if len(parts) < 2:
                        dur = timedelta(minutes=5)
                    else:
                        dur = timedelta(minutes=int(parts[1]))

                    await author.timeout(dur) # type: ignore
                    
                    embed = discord.Embed(
                        description=f"{author.mention} を {int(dur.total_seconds() // 60)} 分間タイムアウトしました。",
                        color=discord.Colour.green()
                    )
                    await message.reply(embed=embed)

                if message.content.startswith(";kick"):
                    reference = message.reference
                    if not reference or not reference.message_id:
                        return
                    
                    reference_message = await message.channel.fetch_message(reference.message_id)
                    if not reference_message:
                        return
                    
                    target = await message.guild.fetch_member(reference_message.author.id)
                    author = target or reference_message.author
                    
                    await author.kick()
                    
                    embed = discord.Embed(
                        description=f"{author.mention} をキックしました。",
                        color=discord.Colour.green()
                    )
                    await message.reply(embed=embed)
                
                if message.content.startswith(";ban"):
                    reference = message.reference
                    if not reference or not reference.message_id:
                        return
                    
                    reference_message = await message.channel.fetch_message(reference.message_id)
                    if not reference_message:
                        return
                    
                    target = await message.guild.fetch_member(reference_message.author.id)
                    author = target or reference_message.author
                    
                    await author.ban()
                    
                    embed = discord.Embed(
                        description=f"{author.mention} を禁止しました。",
                        color=discord.Colour.green()
                    )
                    await message.reply(embed=embed)
                    
        except Exception as e:
            Log.error(e, exc_info=True)
            embed = discord.Embed(
                description="処理中に例外が発生しました。",
                color=discord.Colour.red()
            )
            await message.reply(embed=embed)
                    
async def setup(bot: commands.Bot):
    await bot.add_cog(On_Message(bot))