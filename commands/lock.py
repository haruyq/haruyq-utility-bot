import discord
from discord.ext import commands
from discord import app_commands

from mod.logger import Logger

Log = Logger(__name__)

class LockCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="lock", description="Lock a channel to prevent sending messages.")
    @app_commands.checks.has_permissions(administrator=True)
    async def lock(self, interaction: discord.Interaction):
        if not interaction.guild:
            return
        
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("このコマンドはテキストチャンネルでのみ使用できます。", ephemeral=True)
            return

        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            description=f"チャンネル {channel.mention} は管理者によりロックされました。",
            color=discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)