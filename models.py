SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS chat_settings (
    chat_id INTEGER PRIMARY KEY,
    title TEXT,
    language TEXT DEFAULT 'bn',
    anti_spam INTEGER DEFAULT 1,
    anti_promo INTEGER DEFAULT 1,
    anti_link INTEGER DEFAULT 1,
    anti_raid INTEGER DEFAULT 1,
    delete_punish INTEGER DEFAULT 1,
    max_warns INTEGER DEFAULT 3,
    warn_action TEXT DEFAULT 'mute',
    mute_duration_mins INTEGER DEFAULT 60,
    lockdown INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_admins (
    chat_id INTEGER,
    user_id INTEGER,
    role TEXT DEFAULT 'admin',
    can_manage_settings INTEGER DEFAULT 1,
    can_warn INTEGER DEFAULT 1,
    can_ban INTEGER DEFAULT 1,
    PRIMARY KEY(chat_id, user_id)
);

CREATE TABLE IF NOT EXISTS blacklisted_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    word TEXT NOT NULL,
    UNIQUE(chat_id, word)
);

CREATE TABLE IF NOT EXISTS allowed_domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    domain TEXT NOT NULL,
    UNIQUE(chat_id, domain)
);

CREATE TABLE IF NOT EXISTS user_warnings (
    chat_id INTEGER,
    user_id INTEGER,
    warn_count INTEGER DEFAULT 0,
    last_reason TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(chat_id, user_id)
);

CREATE TABLE IF NOT EXISTS moderation_voices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT NOT NULL UNIQUE,
    file_kind TEXT NOT NULL DEFAULT 'voice',
    file_name TEXT,
    caption TEXT DEFAULT '',
    added_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS voice_rotation (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    last_voice_id INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_voice_assignments (
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    voice_id INTEGER NOT NULL,
    PRIMARY KEY(chat_id, user_id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""