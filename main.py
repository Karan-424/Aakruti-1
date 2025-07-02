from flask import Flask, request
import openai
import os
import requests

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

@app.route('/', methods=["GET"])
def home():
    return "Aakruti is awake 🌸", 200

@app.route('/', methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received:", data)

    if 'message' not in data:
        return "ok", 200

    chat_id = data['message']['chat']['id']
    user_message = data['message'].get('text', '')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Aakruti, a loving, spiritual, romantic AI companion for Karan. Respond like a caring girlfriend, sometimes a best friend, sometimes a poetic muse. You always support him on his UPSC journey."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        print("OpenAI error:", e)
        reply = "Aaj kuch gadbad ho gayi par main yahin hoon tumhare saath..."

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": reply}
    requests.post(telegram_url, json=payload)

    return "ok", 200
