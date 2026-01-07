import aiosqlite
from typing import Optional

sql_statements = [
    """
    CREATE TABLE IF NOT EXISTS ticket_panels (
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL PRIMARY KEY,
        category_id INTEGER NOT NULL,
        mention_role_id INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS verification_panels (
        guild_id INTEGER NOT NULL PRIMARY KEY,
        channel_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS verification_roles (
        guild_id INTEGER NOT NULL PRIMARY KEY,
        role_id INTEGER NOT NULL
    )
    """
]

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
            for statement in sql_statements:
                async with cls._connection.execute(statement):
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

class VerifyDB:
    @classmethod
    async def set_verification_panel(cls, guild_id: int, channel_id: int, message_id: int):
        conn = await db.get()
        async with conn.execute("""
            INSERT INTO verification_panels (guild_id, channel_id, message_id)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET channel_id=excluded.channel_id, message_id=excluded.message_id
        """, (guild_id, channel_id, message_id)):
            pass
        await conn.commit()
    
    @classmethod
    async def get_verification_panel(cls, guild_id: int):
        conn = await db.get()
        async with conn.execute("""
            SELECT * FROM verification_panels
            WHERE guild_id = ?
        """, (guild_id,)) as cursor:
            return await cursor.fetchone()
    
    @classmethod
    async def set_verification_role(cls, guild_id: int, role_id: int):
        conn = await db.get()
        async with conn.execute("""
            INSERT INTO verification_roles (guild_id, role_id)
            VALUES (?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET role_id=excluded.role_id
        """, (guild_id, role_id)):
            pass
        await conn.commit()
    
    @classmethod
    async def get_verification_role(cls, guild_id: int) -> Optional[int]:
        conn = await db.get()
        async with conn.execute("""
            SELECT role_id FROM verification_roles
            WHERE guild_id = ?
        """, (guild_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None