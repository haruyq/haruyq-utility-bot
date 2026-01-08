import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional

from views.embed import BuildEmbedModal

class EmbedCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="send-embed", description="埋め込みメッセージを送信します。")
    @app_commands.default_permissions(administrator=True)
    async def send_embed(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]) -> None:
        await interaction.response.send_modal(
            BuildEmbedModal(
                channel=channel or interaction.channel # type: ignore
            )
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EmbedCommand(bot))