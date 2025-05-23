import requests
import time
import os
from datetime import datetime

API_URL = 'https://alif.tj/api/rates/history?currency=rub&date='

prev_rate = None

def get_rub_rate():
    today = datetime.now().strftime('%Y-%m-%d')
    url = API_URL + today
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list):
            return float(data[0]['moneyTransferBuyValue'])
    except Exception as e:
        print(f"[!] Ошибка при получении курса: {e}")
    return None

def send_telegram_message(text):
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    telegram_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    try:
        response = requests.get(telegram_url, params=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Ошибка при отправке Telegram-сообщения: {e}")
print(f"[INFO] Скрипт запущен и проверяет курс...")
while True:
    print("v cik")
    rate = get_rub_rate()
    if rate is not None:
        if prev_rate is not None or rate != prev_rate:
            send_telegram_message(f"📢 Курс RUB (покупка переводом) изменился: {prev_rate} → {rate}")
        prev_rate = rate
    else:
        print("[-] Не удалось получить курс RUB.")
    
    time.sleep(600)
