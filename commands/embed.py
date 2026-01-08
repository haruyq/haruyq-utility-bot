import discord
from discord.ext import commands
from discord import app_commands

from views.embed import BuildEmbedModal

class EmbedCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="send-embed", description="埋め込みメッセージを送信します。")
    @app_commands.default_permissions(administrator=True)
    async def send_embed(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BuildEmbedModal())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EmbedCommand(bot))