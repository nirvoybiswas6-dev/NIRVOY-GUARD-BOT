import aiosqlite
from typing import Optional, Dict, Any, List
from config import DATABASE_PATH
from database.models import SCHEMA_SQL
from utils.logger import log

class Database:
    def __init__(self, db_path: str = str(DATABASE_PATH)):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.executescript(SCHEMA_SQL)
            # Upgrade existing databases without deleting saved voices/settings.
            cur = await conn.execute("PRAGMA table_info(moderation_voices)")
            columns = {row[1] for row in await cur.fetchall()}
            if "caption" not in columns:
                await conn.execute("ALTER TABLE moderation_voices ADD COLUMN caption TEXT DEFAULT ''")
            await conn.execute("INSERT OR IGNORE INTO voice_rotation (id, last_voice_id) VALUES (1, 0)")
            await conn.commit()
            log.info("ডেটাবেস স্কিমা সফলভাবে সিঙ্ক ও লোড হয়েছে।")

    async def get_chat_settings(self, chat_id: int) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                "SELECT * FROM chat_settings WHERE chat_id = ?", (chat_id,)
            )
            row = await cursor.fetchone()
            if not row:
                await conn.execute(
                    "INSERT INTO chat_settings (chat_id, title) VALUES (?, ?)",
                    (chat_id, "Unknown"),
                )
                await conn.commit()
                cursor = await conn.execute(
                    "SELECT * FROM chat_settings WHERE chat_id = ?", (chat_id,)
                )
                row = await cursor.fetchone()
            return dict(row)

    async def update_chat_setting(self, chat_id: int, key: str, value: Any):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                f"UPDATE chat_settings SET {key} = ? WHERE chat_id = ?",
                (value, chat_id)
            )
            await conn.commit()

    async def add_blacklisted_word(self, chat_id: int, word: str) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.execute(
                    "INSERT INTO blacklisted_words (chat_id, word) VALUES (?, ?)",
                    (chat_id, word.lower().strip())
                )
                await conn.commit()
                return True
        except Exception:
            return False

    async def remove_blacklisted_word(self, chat_id: int, word: str) -> bool:
        async with aiosqlite.connect(self.db_path) as conn:
            cur = await conn.execute(
                "DELETE FROM blacklisted_words WHERE chat_id = ? AND word = ?",
                (chat_id, word.lower().strip())
            )
            await conn.commit()
            return cur.rowcount > 0

    async def get_blacklisted_words(self, chat_id: int) -> List[str]:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT word FROM blacklisted_words WHERE chat_id = ?", (chat_id,)
            )
            rows = await cursor.fetchall()
            return [r[0] for r in rows]

    async def add_allowed_domain(self, chat_id: int, domain: str) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.execute(
                    "INSERT INTO allowed_domains (chat_id, domain) VALUES (?, ?)",
                    (chat_id, domain.lower().strip())
                )
                await conn.commit()
                return True
        except Exception:
            return False

    async def remove_allowed_domain(self, chat_id: int, domain: str) -> bool:
        async with aiosqlite.connect(self.db_path) as conn:
            cur = await conn.execute(
                "DELETE FROM allowed_domains WHERE chat_id = ? AND domain = ?",
                (chat_id, domain.lower().strip())
            )
            await conn.commit()
            return cur.rowcount > 0

    async def get_allowed_domains(self, chat_id: int) -> List[str]:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT domain FROM allowed_domains WHERE chat_id = ?", (chat_id,)
            )
            rows = await cursor.fetchall()
            return [r[0] for r in rows]

    async def log_action(self, chat_id: int, user_id: int, action: str, details: str):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                "INSERT INTO audit_logs (chat_id, user_id, action, details) VALUES (?, ?, ?, ?)",
                (chat_id, user_id, action, details)
            )
            await conn.commit()

    async def add_moderation_voice(self, file_id: str, file_kind: str, file_name: str, added_by: int, caption: str = "") -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.execute(
                    "INSERT INTO moderation_voices (file_id, file_kind, file_name, caption, added_by) VALUES (?, ?, ?, ?, ?)",
                    (file_id, file_kind, file_name or "ভয়েস", (caption or "").strip()[:1024], added_by),
                )
                await conn.commit()
                return True
        except Exception as e:
            log.warning(f"ভয়েস সংরক্ষণ ব্যর্থ: {e}")
            return False

    async def get_moderation_voices(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            cur = await conn.execute("SELECT id, file_id, file_kind, file_name, caption FROM moderation_voices ORDER BY id")
            return [dict(row) for row in await cur.fetchall()]

    async def delete_moderation_voice(self, voice_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as conn:
            cur = await conn.execute("DELETE FROM moderation_voices WHERE id = ?", (voice_id,))
            await conn.execute("DELETE FROM user_voice_assignments WHERE voice_id = ?", (voice_id,))
            await conn.commit()
            return cur.rowcount > 0

    async def get_next_moderation_voice(self) -> Optional[Dict[str, Any]]:
        """Return saved voices in strict insertion order, wrapping to the first."""
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            await conn.execute("BEGIN IMMEDIATE")
            cur = await conn.execute("SELECT last_voice_id FROM voice_rotation WHERE id = 1")
            row = await cur.fetchone()
            last_id = int(row[0]) if row else 0
            cur = await conn.execute(
                "SELECT id, file_id, file_kind, file_name, caption FROM moderation_voices WHERE id > ? ORDER BY id LIMIT 1",
                (last_id,),
            )
            voice = await cur.fetchone()
            if voice is None:
                cur = await conn.execute("SELECT id, file_id, file_kind, file_name, caption FROM moderation_voices ORDER BY id LIMIT 1")
                voice = await cur.fetchone()
            if voice is None:
                await conn.commit()
                return None
            await conn.execute("INSERT OR REPLACE INTO voice_rotation (id, last_voice_id) VALUES (1, ?)", (voice["id"],))
            await conn.commit()
            return dict(voice)

    async def get_voice_for_user(self, chat_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Assign a different random voice to each member in a chat where possible."""
        import random
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            cur = await conn.execute(
                "SELECT v.id, v.file_id, v.file_kind, v.file_name FROM user_voice_assignments a "
                "JOIN moderation_voices v ON v.id = a.voice_id WHERE a.chat_id = ? AND a.user_id = ?",
                (chat_id, user_id),
            )
            row = await cur.fetchone()
            if row:
                return dict(row)
            cur = await conn.execute(
                "SELECT id, file_id, file_kind, file_name FROM moderation_voices "
                "WHERE id NOT IN (SELECT voice_id FROM user_voice_assignments WHERE chat_id = ?)",
                (chat_id,),
            )
            voices = [dict(r) for r in await cur.fetchall()]
            if not voices:
                cur = await conn.execute("SELECT id, file_id, file_kind, file_name FROM moderation_voices")
                voices = [dict(r) for r in await cur.fetchall()]
            if not voices:
                return None
            voice = random.choice(voices)
            await conn.execute(
                "INSERT OR REPLACE INTO user_voice_assignments (chat_id, user_id, voice_id) VALUES (?, ?, ?)",
                (chat_id, user_id, voice["id"]),
            )
            await conn.commit()
            return voice

db = Database()