import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config import BOT_TOKEN
from database.db import db
from utils.logger import log
from handlers.start import start_handler
from handlers.admin import secret_key_receiver
from handlers.commands import (
    warn_command,
    mute_command,
    unmute_command,
    ban_command,
    unban_command
)
from handlers.moderation import group_moderation_handler, member_join_handler
from handlers.callbacks import callback_handler
from handlers.ai_chat import ai_text_handler, ai_command, ai_status_command
from handlers.voices import upload_voice_handler

async def post_init(application):
    await db.init()
    log.info("🛡️ NIRVOY GUARD PRO ইঞ্জিন সফলভাবে প্রস্তুত ও সক্রিয় হয়েছে!")

def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        # AI analysis is asynchronous; allow other Telegram updates to be
        # processed while one message is waiting for Gemini.
        .concurrent_updates(16)
        .build()
    )

    # ১. অথেনটিকেশন ও স্টার্ট কমান্ড
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("ai", ai_command))
    app.add_handler(CommandHandler("aistatus", ai_status_command))
    # AI admin chat handler আগে রাখা হয়েছে; awaiting_ai না থাকলে এটি নিজেই return করবে
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, ai_text_handler))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, secret_key_receiver))
    # Owner/admin can upload Telegram voice notes, audio files, or audio documents to the private bot chat.
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & (filters.VOICE | filters.AUDIO | filters.Document.ALL), upload_voice_handler))

    # ২. মডারেশন কমান্ড
    app.add_handler(CommandHandler("warn", warn_command))
    app.add_handler(CommandHandler("mute", mute_command))
    app.add_handler(CommandHandler("unmute", unmute_command))
    app.add_handler(CommandHandler("ban", ban_command))
    app.add_handler(CommandHandler("unban", unban_command))

    # ৩. ব্যাকগ্রাউন্ড গ্রুপ সিকিউরিটি ফিল্টার
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & (filters.TEXT | filters.CAPTION) & ~filters.COMMAND, group_moderation_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, member_join_handler))

    # ৪. ইন্টারঅ্যাক্টিভ ইনলাইন কিবোর্ড কলব্যাক
    app.add_handler(CallbackQueryHandler(callback_handler))

    log.info("বট পোলিং শুরু হচ্ছে...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()