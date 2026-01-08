import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram import (Update, BotCommand, BotCommandScopeChat, MenuButtonCommands, InlineKeyboardButton,
                      InlineKeyboardMarkup)


def load_message(name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    message_path = os.path.join(current_dir, 'resources', 'messages', f'{name}.txt')
    with open(message_path, "r", encoding="utf-8") as file:
        return file.read()


async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    text = text.encode('utf8').decode('utf8')
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )


async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'resources', 'images', f'{name}.jpg')
    with open(image_path, 'rb') as image:
        return await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image
        )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, commands: dict):
    command_list = [
        BotCommand(command=key, description=value)
        for key, value in commands.items()
    ]
    await context.bot.set_my_commands(
        command_list,
        scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )
    await context.bot.set_chat_menu_button(
        menu_button=MenuButtonCommands(),
        chat_id=update.effective_chat.id
    )


def load_prompt(name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, 'resources', 'prompts', f'{name}.txt')
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


async def send_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, buttons: dict):
    text = text.encode('utf8', errors='surrogatepass').decode('utf8')
    keyboard = []
    for key, value in buttons.items():
        button = InlineKeyboardButton(str(value), callback_data=str(key))
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return await context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=text,
        reply_markup=reply_markup,
        message_thread_id=update.effective_message.message_thread_id)


async def download_voice_message(voice):
    voice_file = await voice.get_file()
    ogg_path = f"voice_{voice.file_id}.ogg"
    await voice_file.download_to_drive(ogg_path)
    return ogg_path


def convert_ogg_to_wav(ogg_file_path):
    wav_file_path = ogg_file_path.replace(".ogg", ".wav")
    audio = AudioSegment.from_ogg(ogg_file_path)
    audio.export(wav_file_path, format="wav")
    return wav_file_path


def cleanup_files(*file_paths):
    for file_path in file_paths:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


def recognize_speech(wav_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='uk-UA')
        return text


def text_to_speech(text, output_file="response.mp3", language='uk'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)
    return output_file