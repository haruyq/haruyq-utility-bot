import discord
from typing import Any

class TicketSettings:
    def __init__(self) -> None:
        self.title = "未設定"
        self.description = "未設定"
        self.channel = "未設定"
        self.category = "未設定"
        self.mention = "未設定"
    
    def as_text(self) -> str:
        return "\n".join([
            f"**タイトル**: {self.title}",
            f"**説明**: {self.description}",
            f"**チャンネル**: {self.channel}",
            f"**カテゴリー**: {self.category}",
            f"**メンション**: {self.mention}",
        ])

class TicketTitleModal(discord.ui.Modal, title="チケットタイトル設定"):
    def __init__(self, parent: "TicketSetupView"):
        super().__init__()
        self.parent = parent
        
        self.title_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="タイトル",
            placeholder="パネルのタイトルを入力してください",
            required=True,
            max_length=50
        )
        
        self.add_item(self.title_input)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        title = self.title_input.value.strip() or "未設定"
        self.parent.settings.title = title
        await self.parent.refresh()
        await interaction.response.send_message(f"チケットパネルのタイトルが **{title}** に設定されました。", ephemeral=True)

class TicketDescriptionModal(discord.ui.Modal, title="チケット説明設定"):
    def __init__(self, parent: "TicketSetupView"):
        super().__init__()
        self.parent = parent
        
        self.description_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="説明",
            placeholder="パネルの説明を入力してください",
            style=discord.TextStyle.long,
            required=False,
            max_length=4000
        )
        
        self.add_item(self.description_input)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        description = self.description_input.value.strip() or "未設定"
        self.parent.settings.description = description
        await self.parent.refresh()
        await interaction.response.send_message("チケットパネルの説明を更新しました。", ephemeral=True)

class TicketChannelModal(discord.ui.Modal, title="チケットチャンネル設定"):
    def __init__(self, parent: "TicketSetupView"):
        super().__init__()
        self.parent = parent
        
        self.channel_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="チャンネル",
            placeholder="#general や ID を入力してください",
            required=False,
            max_length=100
        )
        
        self.add_item(self.channel_input)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        raw_value = self.channel_input.value.strip()
        if not raw_value:
            self.parent.settings.channel = "未設定"
            await self.parent.refresh()
            await interaction.response.send_message("チャンネル設定をリセットしました。", ephemeral=True)
            return
        
        guild = interaction.guild
        channel = self.parent.resolve_text_channel(guild, raw_value)
        if channel is None:
            await interaction.response.send_message("有効なテキストチャンネルを入力してください。", ephemeral=True)
            return
        
        self.parent.settings.channel = channel.mention
        await self.parent.refresh()
        await interaction.response.send_message(f"送信チャンネルを {channel.mention} に設定しました。", ephemeral=True)

class TicketCategoryModal(discord.ui.Modal, title="チケットカテゴリー設定"):
    def __init__(self, parent: "TicketSetupView"):
        super().__init__()
        self.parent = parent
        
        self.category_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="カテゴリー",
            placeholder="カテゴリーのメンションまたは ID を入力してください",
            required=False,
            max_length=100
        )
        
        self.add_item(self.category_input)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        raw_value = self.category_input.value.strip()
        if not raw_value:
            self.parent.settings.category = "未設定"
            await self.parent.refresh()
            await interaction.response.send_message("カテゴリー設定をリセットしました。", ephemeral=True)
            return
        
        guild = interaction.guild
        category = self.parent.resolve_category(guild, raw_value)
        if category is None:
            await interaction.response.send_message("有効なカテゴリーを入力してください。", ephemeral=True)
            return
        
        self.parent.settings.category = category.name
        await self.parent.refresh()
        await interaction.response.send_message(f"カテゴリーを {category.name} に設定しました。", ephemeral=True)

class TicketMentionModal(discord.ui.Modal, title="メンション設定"):
    def __init__(self, parent: "TicketSetupView"):
        super().__init__()
        self.parent = parent
        
        self.mention_input: discord.ui.TextInput[Any] = discord.ui.TextInput(
            label="メンション",
            placeholder="@everyone や ロール/ユーザーを入力してください",
            required=False,
            max_length=100
        )
        
        self.add_item(self.mention_input)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        raw_value = self.mention_input.value.strip()
        if not raw_value:
            self.parent.settings.mention = "未設定"
            await self.parent.refresh()
            await interaction.response.send_message("メンション設定をリセットしました。", ephemeral=True)
            return
        
        mention = self.parent.resolve_mention(interaction.guild, raw_value)
        if mention is None:
            await interaction.response.send_message("有効なメンションを入力してください。", ephemeral=True)
            return
        
        self.parent.settings.mention = mention
        await self.parent.refresh()
        await interaction.response.send_message(f"メンションを {mention} に設定しました。", ephemeral=True)

class TicketSetupView(discord.ui.View):
    def __init__(self, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.settings = TicketSettings()
        self.original_msg: discord.Message | None = None
        
    def set_original_msg(self, msg: discord.Message) -> None:
        self.original_msg = msg
    
    def build_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="チケットパネル設定",
            description="以下のボタンからチケットパネルの設定を行ってください。",
            color=discord.Colour.blue()
        )
        
        embed.add_field(name="現在の設定", value=self.settings.as_text(), inline=False)
        return embed
    
    async def refresh(self) -> None:
        if self.original_msg is None:
            return
        
        await self.original_msg.edit(embed=self.build_embed(), view=self)
    
    @staticmethod
    def _extract_id(value: str) -> int | None:
        digits = "".join(ch for ch in value if ch.isdigit())
        return int(digits) if digits else None
    
    def resolve_text_channel(self, guild: discord.Guild | None, raw: str) -> discord.TextChannel | None:
        if guild is None:
            return None
        channel_id = self._extract_id(raw)
        if channel_id is not None:
            channel = guild.get_channel(channel_id)
            if isinstance(channel, discord.TextChannel):
                return channel
        return discord.utils.get(guild.text_channels, name=raw)
    
    def resolve_category(self, guild: discord.Guild | None, raw: str) -> discord.CategoryChannel | None:
        if guild is None:
            return None
        category_id = self._extract_id(raw)
        if category_id is not None:
            channel = guild.get_channel(category_id)
            if isinstance(channel, discord.CategoryChannel):
                return channel
        return discord.utils.get(guild.categories, name=raw)
    
    def resolve_mention(self, guild: discord.Guild | None, raw: str) -> str | None:
        lowered = raw.lower()
        if lowered in {"@everyone", "everyone"}:
            return "@everyone"
        if lowered in {"@here", "here"}:
            return "@here"
        target_id = self._extract_id(raw)
        if target_id is None or guild is None:
            return None
        role = guild.get_role(target_id)
        if role is not None:
            return role.mention
        member = guild.get_member(target_id)
        if member is not None:
            return member.mention
        return None
    
    @discord.ui.button(label="タイトル設定", style=discord.ButtonStyle.primary, custom_id="ticket_setup:set_title")
    async def set_title(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketSetupView"]) -> None:
        await interaction.response.send_modal(TicketTitleModal(self))
    
    @discord.ui.button(label="説明設定", style=discord.ButtonStyle.primary, custom_id="ticket_setup:set_description")
    async def set_description(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketSetupView"]) -> None:
        await interaction.response.send_modal(TicketDescriptionModal(self))
    
    @discord.ui.button(label="チャンネル設定", style=discord.ButtonStyle.primary, custom_id="ticket_setup:set_channel")
    async def set_channel(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketSetupView"]) -> None:
        await interaction.response.send_modal(TicketChannelModal(self))
    
    @discord.ui.button(label="カテゴリー設定", style=discord.ButtonStyle.primary, custom_id="ticket_setup:set_category")
    async def set_category(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketSetupView"]) -> None:
        await interaction.response.send_modal(TicketCategoryModal(self))
    
    @discord.ui.button(label="メンション設定", style=discord.ButtonStyle.primary, custom_id="ticket_setup:set_mention")
    async def set_mention(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketSetupView"]) -> None:
        await interaction.response.send_modal(TicketMentionModal(self))
    
    @discord.ui.button(label="送信", style=discord.ButtonStyle.green, custom_id="ticket_setup:complete")
    async def complete(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketSetupView"]) -> None:
        embed = discord.Embed(
            title=self.settings.title,
            description=self.settings.description,
            color=discord.Colour.green()
        )
        channel = self.resolve_text_channel(interaction.guild, self.settings.channel)
        if not channel:
            await interaction.response.send_message("有効な送信チャンネルが設定されていません。", ephemeral=True)
            return
        
        await channel.send(embed=embed)
        
        await interaction.response.send_message("チケットパネルが送信されました。", ephemeral=True)
        self.stop()