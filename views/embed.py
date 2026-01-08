import discord

from typing import Any

class BuildEmbedModal(discord.ui.Modal, title="埋め込みメッセージの作成"):
    def __init__(self):
        super().__init__()
        self.title_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="タイトル",
            placeholder="埋め込みメッセージのタイトルを入力してください",
            max_length=256,
        )
        self.description_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="説明",
            style=discord.TextStyle.paragraph,
            placeholder="埋め込みメッセージの説明を入力してください",
            max_length=2048,
        )
        self.add_item(self.title_input)
        self.add_item(self.description_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description_input.value,
            color=discord.Colour.blue(),
        )
        
        if isinstance(interaction.channel, discord.TextChannel):
            await interaction.channel.send(embed=embed)