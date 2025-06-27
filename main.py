import requests
import os
from datetime import datetime

API_URL = 'https://alif.tj/api/rates/history?currency=rub&date='
RATE_FILE = 'prev_rate.txt'

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

def load_prev_rate():
    if os.path.exists(RATE_FILE):
        try:
            with open(RATE_FILE, 'r') as file:
                return float(file.read().strip())
        except Exception as e:
            print(f"[!] Ошибка при чтении файла курса: {e}")
    return None

def save_prev_rate(rate):
    try:
        with open(RATE_FILE, 'w') as file:
            file.write(str(rate))
    except Exception as e:
        print(f"[!] Ошибка при сохранении курса: {e}")

if __name__ == "__main__":
    print("[INFO] Скрипт запущен.")
    
    prev_rate = load_prev_rate()
    rate = get_rub_rate()

    if rate is not None:
        if prev_rate is None:
            print(f"[INFO] Сохранён текущий курс: {rate}")
            save_prev_rate(rate)
        elif rate != prev_rate:
            send_telegram_message(f"📢 Курс RUB (покупка переводом) изменился: {prev_rate} → {rate}")
            save_prev_rate(rate)
            print(f"[INFO] Курс изменился и обновлён в файле.")
        else:
            print(f"[INFO] Курс не изменился: {rate}")
    else:
        print("[!] Не удалось получить текущий курс RUB.")
