from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

SMARTCAPTCHA_SERVER_KEY = "ysc2_G6HSMHbwOOZhDZbyHCbQB5i2BhdbqXOcQBNMirdcf9b8ab6a"

# тестовый эндпоинт
@app.route('/', methods=['GET'])
def helo():
    return "Hello from CAPTCHA App", 200

# эндпоинт, возвращающий страницу для встраивания капчи
@app.route('/captcha', methods=['GET'])
def render_captcha():
    return render_template("captcha.html")

# эндпоинт валидации результата прохождения капчи
@app.route('/validate-captcha', methods=['POST'])
def validate_captcha():
    data = request.json
    token = data.get('token')

    if not token:
        return jsonify({"status": "error", "message": "Missing CAPTCHA token"}), 400

    # валидация ответа
    response = requests.post(
        "https://smartcaptcha.yandexcloud.net/validate",
        data={
            "secret": SMARTCAPTCHA_SERVER_KEY,
            "token": token,
            "ip": request.remote_addr  # Optional: get user's IP
        },
        timeout=2
    )

    if response.status_code != 200:
        return jsonify({"status": "error", "message": "Captcha validation error"}), 500

    # обработка ответа
    captcha_result = response.json()
    if captcha_result.get("status") == "ok":
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "robot"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
