import discord

from typing import Any

from mod.db import VerifyDB
from mod.gen_cap import generate_captcha

class AnswerModal(discord.ui.Modal, title="画像の数字を入力して下さい"):
    def __init__(self, answer: int):
        super().__init__()
        self.answer_value = answer
        self.answer: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="画像の数字を入力してください",
            placeholder="12345",
            max_length=5,
        )
        self.add_item(self.answer)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        if not interaction.guild:
            return
        
        if self.answer.value != str(self.answer_value):
            await interaction.response.send_message("認証に失敗しました。もう一度やり直してください。", ephemeral=True)
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
        await interaction.response.send_message("認証が完了しました。", ephemeral=True)

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="✅｜認証する", style=discord.ButtonStyle.blurple, custom_id="verify:verify_btn")
    async def verify_btn(self, interaction: discord.Interaction, _button: discord.ui.Button["VerifyView"]) -> None:
        if not interaction.guild:
            return
        
        img_data, answer = generate_captcha()
        file = discord.File(fp=img_data, filename="captcha.png")
        
        embed = discord.Embed(
            description="以下の画像に表示されている数字を入力してください。",
            color=discord.Colour.blue(),
        )
        embed.set_image(url="attachment://captcha.png")
        await interaction.response.send_message(embed=embed, file=file, view=AnswerView(answer), ephemeral=True)

class AnswerView(discord.ui.View):
    def __init__(self, answer: int):
        super().__init__()
        self.answer = answer

    @discord.ui.button(label="答えを入力する", style=discord.ButtonStyle.gray, custom_id="verify:answer_btn")
    async def answer_btn(self, interaction: discord.Interaction, _button: discord.ui.Button["AnswerView"]) -> None:
        await interaction.response.send_modal(AnswerModal(self.answer))