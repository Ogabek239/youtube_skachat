import os
import telebot
import yt_dlp
from moviepy import AudioFileClip
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '7681275010:AAEVd1KZYUiieImNzIGn4m2hKx4zjAvYqDM'
bot = telebot.TeleBot(BOT_TOKEN)

user_links = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom jigarim! 🎬 Menga YouTube yoki Instagram link yubor. Men video va musiqani chiqarib beraman.")

@bot.message_handler(func=lambda msg: True)
def handle_link(message):
    url = message.text

    if "youtube.com" in url or "youtu.be" in url or "instagram.com" in url:
        user_links[message.chat.id] = url

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🎥 Video", callback_data="get_video"),
            InlineKeyboardButton("🎵 Musiqa", callback_data="get_audio")
        )
        bot.send_message(message.chat.id, "Qaysi formatda yuboray?", reply_markup=markup)
    else:
        bot.reply_to(message, "Faqat YouTube yoki Instagram link yuboring.")

@bot.callback_query_handler(func=lambda call: True)
def handle_download(call):
    url = user_links.get(call.message.chat.id)
    if not url:
        bot.answer_callback_query(call.id, "Link topilmadi.")
        return

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="⏬ Yuklanmoqda...")

    output_path = "media"
    os.makedirs(output_path, exist_ok=True)

    try:
        ydl_opts = {
            'outtmpl': os.path.join(output_path, 'video.%(ext)s'),
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        if call.data == "get_video":
            with open(video_path, 'rb') as video:
                bot.send_video(call.message.chat.id, video)
        elif call.data == "get_audio":
            audio_path = os.path.join(output_path, 'audio.mp3')
            audioclip = AudioFileClip(video_path)
            audioclip.write_audiofile(audio_path)

            with open(audio_path, 'rb') as audio:
                bot.send_audio(call.message.chat.id, audio)

            os.remove(audio_path)

        os.remove(video_path)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Xatolik: {e}")

bot.polling()