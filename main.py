from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Укажите ваш Telegram Bot Token и chat_id
TELEGRAM_API_URL = "https://api.telegram.org/bot<8489651453:AAF-9pbgHvlHpbJ8gbXMvXAHEhpEC4a_s_U>/sendMessage"
CHAT_ID = "<@xfxki>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()  # Получаем данные из POST запроса
    message = data.get('message')  # Извлекаем сообщение
    send_to_telegram(message)  # Отправляем сообщение в Telegram
    return jsonify({"status": "success"})

def send_to_telegram(message):
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(TELEGRAM_API_URL, data=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

if __name__ == '__main__':
    app.run(debug=True)