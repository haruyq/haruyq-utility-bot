import discord
from discord.ext import commands

import os

from mod.logger import Logger
from mod.db import db

Log = Logger(__name__)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        try:
            if not os.path.exists("./db"):
                os.mkdir("./db")
            
            if not os.path.exists("./db/main.db"):
                await db.init()
            
            for f in os.listdir("./commands"):
                if f.endswith(".py"):
                    await self.load_extension(f"commands.{f[:-3]}")
                    Log.info(f"[Command] Loaded: {f}")
            
            for f in os.listdir("./events"):
                if f.endswith(".py"):
                    await self.load_extension(f"events.{f[:-3]}")
                    Log.info(f"[Event] Loaded: {f}")
                    
        except Exception as e:
            Log.error(e, exc_info=True)
                
bot = MyBot()

token = os.environ.get("TOKEN", None)
if token:
    bot.run(token, log_handler=None)

else:
    from dotenv import load_dotenv
    load_dotenv("./config/.env")
    bot.run(os.getenv("TOKEN", ""))
