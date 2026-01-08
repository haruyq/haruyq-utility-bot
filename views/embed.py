import discord

from typing import Any

class BuildEmbedModal(discord.ui.Modal, title="埋め込みメッセージの作成"):
    def __init__(self):
        super().__init__()
        self.title_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="タイトル",
            placeholder="埋め込みメッセージのタイトルを入力してください",
            max_length=256,
            required=False,
        )
        self.description_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="説明",
            style=discord.TextStyle.paragraph,
            placeholder="埋め込みメッセージの説明を入力してください",
            max_length=2048,
            required=False,
        )
        self.add_item(self.title_input)
        self.add_item(self.description_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if not interaction.channel:
            return
        
        title = self.title_input.value or None
        description = self.description_input.value or None
        
        if not title and not description:
            await interaction.response.send_message("タイトルまたは説明のいずれかを入力してください。", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.blue(),
        )
        
        msg = None
        if isinstance(interaction.channel, discord.TextChannel):
            msg = await interaction.channel.send(embed=embed)
        
        if msg:
            await interaction.response.send_message(f"埋め込みメッセージを送信しました -> {msg.jump_url}", ephemeral=True)