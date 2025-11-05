from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()  # Получаем данные в формате JSON
    user_input = data.get('user_input')  # Извлекаем текст
    print(f'Полученный текст: {user_input}')  # Выводим на сервере
    return jsonify({"response": user_input})  # Отправляем ответ обратно в формате JSON

if __name__ == '__main__':
    app.run(debug=True)
