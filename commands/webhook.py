import discord
from discord.ext import commands
from discord import app_commands, Webhook

import json
import aiohttp

from typing import Any

from mod.logger import Logger

Log = Logger(__name__)

class WebhookSendContext(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.data: dict[str, Any] = {}
        
        def _make_menu() -> None:
            with open("./config/webhooks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.data = data
                
            webhooks = self.data.get("webhooks", [])
            
            webhooks_count = len(webhooks)
            if webhooks_count == 0:
                return

            if webhooks_count > 5:
                Log.warning("Webhook count exceeds 5, context menu commands will not be created.")
            
            for i in webhooks:
                try:
                    menu = app_commands.ContextMenu(
                        name=str(i['name']),
                        callback=self.send_webhook
                    )
                    self.bot.tree.add_command(menu)
                except Exception as e:
                    Log.error(f"Failed to create context menu for webhook {i.get('name', 'unknown')}: {e}", exc_info=True)
                    continue
        _make_menu()
    
    async def send_webhook(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if (interaction.user != message.author
            or interaction.permissions.administrator == False
            ):
            return
        
        await interaction.response.defer(ephemeral=True)
        
        webhooks = self.data.get("webhooks", [])
        command = interaction.command
        if command is None:
            return

        target_webhook_url: str | None = None
        
        for i in webhooks:
            if i.get("name") == command.name:
                target_webhook_url = i.get("url")
                break

        if not target_webhook_url:
            await interaction.followup.send("WebhookのURLが見つかりませんでした。", ephemeral=True)
            return

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(target_webhook_url, session=session)
            await webhook.send(
                content=message.content,
            )
        
        await interaction.followup.send("メッセージが送信されました。", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WebhookSendContext(bot))