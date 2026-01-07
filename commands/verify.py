import discord
from discord.ext import commands
from discord import app_commands

from views.verify import VerifyView

from mod.db import VerifyDB
from mod.logger import Logger

Log = Logger(__name__)

class VerifyCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="verify-set", description="認証パネルを設置します。")
    @app_commands.default_permissions(administrator=True)
    async def verify_set(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role) -> None:
        if not interaction.guild:
            return
        
        await interaction.response.defer(ephemeral=True)
        
        panel = await VerifyDB.get_verification_panel(interaction.guild.id)
        if panel is not None:
            await interaction.followup.send("既に認証パネルが設置されています。", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="認証パネル",
            color=discord.Colour.green(),
        )
        embed.description = f"""
        認証を完了するとサーバーを閲覧できます。
        付与されるロール: {role.mention}
        """
        embed.set_footer(text="Created by @gptcoder")
        
        await interaction.followup.send(f"認証パネルを {channel.mention} に設置しました。", ephemeral=True)
        
        msg = await channel.send(embed=embed, view=VerifyView())

        await VerifyDB.set_verification_panel(interaction.guild.id, channel.id, msg.id)
        await VerifyDB.set_verification_role(interaction.guild.id, role.id)

async def setup(bot: commands.Bot):
    await bot.add_cog(VerifyCommand(bot))