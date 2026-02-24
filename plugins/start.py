import os, asyncio, humanize
from pyrogram import Client, filters, __version__, enums
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FILE_AUTO_DELETE
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

madflixofficials = FILE_AUTO_DELETE
jishudeveloper = madflixofficials
file_auto_delete = humanize.naturaldelta(jishudeveloper)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    
    text = message.text
    if len(text)>7:
        # --- BATCH / LINK HANDLING ---
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")
        except:
            return

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else range(start, end - 1, -1)
            except:
                return
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return

        temp_msg = await message.reply("<b>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ... ⌛</b>")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something Went Wrong..!")
            return
        await temp_msg.delete()
    
        madflix_msgs = []
        for msg in messages:
            f_name = msg.document.file_name if msg.document else "Movie/File"
            caption = (
                f"<b><i>{f_name}</i></b>\n"
                f"<b><blockquote expandable>➢ Aᴜᴅɪᴏ Tʀᴀᴄᴋ:- 🔊 HINDI / ENG</blockquote></b>\n"
                f"<b><blockquote expandable>➪ sᴜʙᴛɪᴛʟᴇs:- 📝 AVAILABLE</blockquote></b>"
            )

            try:
                madflix_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, protect_content=PROTECT_CONTENT)
                madflix_msgs.append(madflix_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                madflix_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, protect_content=PROTECT_CONTENT)
                madflix_msgs.append(madflix_msg)
            except:
                pass

        k = await client.send_message(chat_id=message.from_user.id, text=f"<b>❗️ <u>IMPORTANT</u> ❗️</b>\n\nThis Video Will Be Deleted In {file_auto_delete}.")
        asyncio.create_task(delete_files(madflix_msgs, client, k))
        return
    
    else:
        # --- NEW ANIMATION LOGIC ---
        # Typing niche text mein dikhayega
        status_msg = await message.reply("<b>ᴛʏᴘɪɴɢ...</b>")
        await asyncio.sleep(1)
        
        # Sticker aayega
        await message.reply_sticker("CAACAgUAAxkBAAECYAlpnPTYKn931L0k_FDtz42O4HE3cwACWRkAAoON0VZunm7nTQJEpzoE")
        await status_msg.delete()
        await asyncio.sleep(0.5)

        # Ab Main Menu khulega
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔵 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🔵", url="http://t.me/File_store_movies_bot?startgroup=true")],
                [InlineKeyboardButton("ℹ️ ʜᴇʟᴘ", callback_data="about"), InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="stats")],
                [InlineKeyboardButton("🌀 sᴜᴘᴘᴏʀᴛ", url="https://t.me/ll_I_sukoon_ll"), InlineKeyboardButton("🌐 ᴄʜᴀɴɴᴇʟ", url="https://t.me/AKDRAMAHUB")],
                [InlineKeyboardButton("🛠️ ʙᴀᴛᴄʜ ᴍᴏᴅᴇ", callback_data="batch_help")]
            ]
        )
        
        await message.reply_photo(
            photo="https://telegra.ph/file/76a0fd6054e0f06536034.jpg",
            caption=START_MSG.format(
                first=message.from_user.first_name,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup
        )
        return
