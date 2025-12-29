import discord
import aiosqlite

from typing import Optional

from mod.db import TicketDB

class TicketCloseView(discord.ui.View):
    def __init__(self, ticket_channel_id: int):
        super().__init__(timeout=None)
        self.ticket_channel_id = ticket_channel_id

    @discord.ui.button(label="🔒｜閉じる", style=discord.ButtonStyle.danger, custom_id="ticket:close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketCloseView"]) -> None:
        if not interaction.guild:
            return
        
        channel = interaction.guild.get_channel(self.ticket_channel_id)
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("チケットチャンネルが見つかりません。", ephemeral=True)
            return
        
        member = interaction.guild.get_member(interaction.user.id)
        if not member:
            await interaction.response.send_message("ユーザー情報が取得できませんでした。", ephemeral=True)
            return
        
        await channel.set_permissions(target=member, read_messages=False, send_messages=False)
        await channel.edit(name=f"closed-{channel.name}", reason="Ticket closed")
        
        await channel.send(f"{member.mention} によりチケットが閉じられました。")
        self.stop()

class TicketView(discord.ui.View):
    def __init__(self, ticket_id: int):
        super().__init__(timeout=None)
        self.ticket_id = ticket_id

    @discord.ui.button(label="🎫｜開く", style=discord.ButtonStyle.green, custom_id="ticket:view_open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketView"]) -> None:
        if not interaction.guild or not interaction.message:
            return
        
        panel_data: Optional[aiosqlite.Row] = await TicketDB.get_panel(interaction.guild.id, interaction.message.id)
        if not panel_data:
            await interaction.response.send_message("このパネルは無効です。", ephemeral=True)
            return
        
        category = interaction.guild.get_channel(panel_data["category_id"])
        if not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message("指定されたカテゴリーが見つかりません。\n管理者にお問い合わせください。", ephemeral=True)
            return
        
        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            reason="This is a ticket channel created by the haruyq-utility-bot."
        )
        
        member = interaction.guild.get_member(interaction.user.id)
        if not member:
            await interaction.response.send_message("ユーザー情報が取得できませんでした。", ephemeral=True)
            return
        
        await channel.set_permissions(target=member, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=False)
        
        embed = discord.Embed(
            title="チケットが作成されました",
            description=f"{interaction.user.mention} さんのチケットです。\nスタッフの対応をお待ちください。",
            color=discord.Colour.green()
        )
        
        mention_role_id: Optional[int] = panel_data["mention_role_id"]
        if mention_role_id:
            mention_role = interaction.guild.get_role(mention_role_id)
            if mention_role:
                await channel.send(f"{mention_role.mention} {member.mention}", embed=embed)