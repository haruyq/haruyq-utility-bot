import discord

from mod.db import VerifyDB

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="✅｜認証する", style=discord.ButtonStyle.blurple)
    async def verify_btn(self, interaction: discord.Interaction, _button: discord.ui.Button["VerifyView"]) -> None:
        if not interaction.guild:
            return
        
        role_id = await VerifyDB.get_verification_role(interaction.guild.id)
        if role_id is None:
            await interaction.response.send_message("認証ロールが設定されていません。", ephemeral=True)
            return
        
        role = interaction.guild.get_role(role_id)
        if role is None:
            try:
                role = await interaction.guild.fetch_role(role_id)
            except discord.NotFound:
                await interaction.response.send_message("認証ロールが見つかりません。", ephemeral=True)
                return
        
        if isinstance(interaction.user, discord.Member):
            member = interaction.user
        else:
            member = await interaction.guild.fetch_member(interaction.user.id)
        
        if role in member.roles:
            await interaction.response.send_message("既に認証されています。", ephemeral=True)
            return
        
        await member.add_roles(role, reason="User verified via verification panel.")
        await interaction.response.send_message("認証が完了しました！", ephemeral=True)