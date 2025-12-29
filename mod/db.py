import aiosqlite
from typing import Optional

sql = """
CREATE TABLE IF NOT EXISTS ticket_panels (
    guild_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    mention_role_id INTEGER
    )
"""

class db:
    _connection: Optional[aiosqlite.Connection] = None

    @classmethod
    async def get(cls) -> aiosqlite.Connection:
        if cls._connection is None:
            cls._connection = await aiosqlite.connect("./db/main.db")
            await cls.init()
        return cls._connection

    @classmethod
    async def init(cls):
        if not cls._connection:
            await cls.get()
        
        if cls._connection:
            async with cls._connection.execute(sql):
                pass
            await cls._connection.commit()

    @classmethod
    async def close(cls):
        if cls._connection is not None:
            await cls._connection.close()
            cls._connection = None
            
class TicketDB:
    @classmethod
    async def add_panel(cls, guild_id: int, channel_id: int, message_id: int, category_id: int, mention_role_id: Optional[int] = None):
        conn = await db.get()
        async with conn.execute("""
            INSERT INTO ticket_panels (guild_id, channel_id, message_id, category_id, mention_role_id)
            VALUES (?, ?, ?, ?, ?)
        """, (guild_id, channel_id, message_id, category_id, mention_role_id)):
            pass
        await conn.commit()
    
    @classmethod
    async def remove_panel(cls, guild_id: int, message_id: int):
        conn = await db.get()
        async with conn.execute("""
            DELETE FROM ticket_panels
            WHERE guild_id = ? AND message_id = ?
        """, (guild_id, message_id)):
            pass
        await conn.commit()
    
    @classmethod
    async def get_panel(cls, guild_id: int, message_id: int):
        conn = await db.get()
        async with conn.execute("""
            SELECT * FROM ticket_panels
            WHERE guild_id = ? AND message_id = ?
        """, (guild_id, message_id)) as cursor:
            return await cursor.fetchone()