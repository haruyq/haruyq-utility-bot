import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional

from mod.logger import Logger

Log = Logger(__name__)

class PurgeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def _check(self, msg: discord.Message, user: discord.User) -> bool:
        return msg.author.id == user.id
    
    @app_commands.command(name="purge", description="メッセージを一括削除します。")
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction, amount: int, user: Optional[discord.User]) -> None:
        if not interaction.guild:
            return
        
        await interaction.response.send_message("メッセージを削除しています...", ephemeral=True)
        
        channel = interaction.channel
        if not isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.Thread)):
            await interaction.response.send_message("このコマンドはテキストチャンネルでのみ使用できます。", ephemeral=True)
            return
        
        try:
            if user:
                await channel.purge(limit=amount, check=lambda msg: self._check(msg, user))
            
            else:
                await channel.purge(limit=amount)
            
        except Exception as e:
            Log.error(f"Purge Failed: {e}", exc_info=True)
            await channel.send("エラーが発生しました。")
            return
        
        embed = discord.Embed(
            description=f"{amount} 件のメッセージが削除されました。",
            color=discord.Colour.green()
        )
        embed.set_footer(text=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        
        await channel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PurgeCommand(bot))