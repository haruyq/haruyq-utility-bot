import discord
from discord.ext import commands
from discord import app_commands

from views.ticket_setup import TicketSetupView

class TicketCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="ticket-set", description="チケットパネルを設置します。")
    @app_commands.default_permissions(administrator=True)
    async def ticket_set(self, interaction: discord.Interaction) -> None:
        view = TicketSetupView()
        await interaction.response.send_message(embed=view.build_embed(), view=view, ephemeral=True)
        
        sent_msg = await interaction.original_response()
        view.set_original_msg(sent_msg)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicketCommand(bot))