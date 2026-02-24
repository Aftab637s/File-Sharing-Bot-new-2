from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>╔════❰ ᴀʙᴏᴜᴛ ᴍᴇ ❱════╗\n\n"
                   f"🤖 Bot Name : <a href='https://t.me/File_store_movies_bot'>File Store Movies Bot</a>\n"
                   f"👑 Owner : <a href='https://t.me/ll_I_sukoon_ll'>Aftab</a>\n"
                   f"🎬 Backup : <a href='https://t.me/AKDRAMAHUB'>AK DRAMA HUB</a>\n"
                   f"🐍 Language : <a href='https://www.python.org/'>Python 3</a>\n"
                   f"📚 Library : <a href='https://docs.pyrogram.org/'>Pyrogram {__version__}</a>\n"
                   f"🚀 Server : <a href='https://www.heroku.com/'>Heroku</a>\n"
                   f"╚══════════════════╝</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
