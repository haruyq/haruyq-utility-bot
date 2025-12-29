import discord
import aiosqlite

from typing import Optional

from mod.logger import Logger
from mod.db import TicketDB

Log = Logger(__name__)

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
        
        await channel.set_permissions(target=interaction.user, read_messages=False, send_messages=False) # type: ignore
        await channel.edit(name=f"closed-{channel.name}", reason="Ticket closed")
        
        await channel.send(f"{interaction.user.mention} によりチケットが閉じられました。")
        self.stop()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫｜開く", style=discord.ButtonStyle.green, custom_id="ticket:view_open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, _button: discord.ui.Button["TicketView"]) -> None:
        if not interaction.guild or not interaction.message:
            return
        
        panel_data: Optional[aiosqlite.Row] = await TicketDB.get_panel(interaction.guild.id, interaction.message.id)
        if not panel_data:
            await interaction.response.send_message("このパネルは無効です。", ephemeral=True)
            return
        
        category_id = panel_data[3]
        category = interaction.guild.get_channel(category_id)
        if not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message("指定されたカテゴリーが見つかりません。\n管理者にお問い合わせください。", ephemeral=True)
            return
        
        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            reason="This is a ticket channel created by the haruyq-utility-bot."
        )
        
        await channel.set_permissions(target=interaction.user, read_messages=True, send_messages=True) # type: ignore
        await channel.set_permissions(interaction.guild.default_role, read_messages=False)
        
        embed = discord.Embed(
            title="チケットが作成されました",
            description=f"{interaction.user.mention} さんのチケットです。\nスタッフの対応をお待ちください。",
            color=discord.Colour.green()
        )
        
        mention_role_id: Optional[int] = panel_data[4]
        if mention_role_id:
            mention_role = interaction.guild.get_role(mention_role_id)
            if mention_role:
                await channel.send(f"{mention_role.mention} {interaction.user.mention}", embed=embed, view=TicketCloseView(channel.id))
            else:
                await channel.send(f"{interaction.user.mention}", embed=embed, view=TicketCloseView(channel.id))