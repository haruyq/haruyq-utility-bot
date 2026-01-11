import discord
from discord.ext import commands
from discord import app_commands

from mod.logger import Logger

Log = Logger(__name__)

class UnLockCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="unlock", description="チャンネルのロックを解除します。")
    @app_commands.checks.has_permissions(administrator=True)
    async def unlock(self, interaction: discord.Interaction):
        if not interaction.guild:
            return
        
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("このコマンドはテキストチャンネルでのみ使用できます。", ephemeral=True)
            return
        
        if not channel.permissions_for(interaction.guild.default_role).send_messages:
            await interaction.response.send_message("このチャンネルはロックされていません。", ephemeral=True)
            return

        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            description=f"チャンネル {channel.mention} は管理者によりロックが解除されました。",
            color=discord.Colour.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnLockCommand(bot))