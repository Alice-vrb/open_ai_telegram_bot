from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler,
                          filters)

from config import BOT_TOKEN
from handlers import (start, random, gpt, message_handler, talk, talk_button, story, story_button,
                      stateless_command_button, voice, voice_handler)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("talk", talk))
app.add_handler(CommandHandler("story", story))
app.add_handler(CommandHandler("voice", voice))
app.add_handler(CallbackQueryHandler(stateless_command_button, pattern='^(start|random|story)$'))
app.add_handler(
    CallbackQueryHandler(
        talk_button,
        pattern='^(talk_linus_torvalds|talk_guido_van_rossum|talk_mark_zuckerberg)$'
    )
)
app.add_handler(CallbackQueryHandler(story_button, pattern='^(dark|light|funny|mystic|random_vibe)$'))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
app.add_handler(MessageHandler(filters.VOICE, voice_handler))

app.run_polling(
    drop_pending_updates=True,
    allowed_updates=Update.ALL_TYPES
)