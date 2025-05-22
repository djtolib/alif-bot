import requests
import time
from datetime import datetime

TOKEN = '7928863499:AAHcSn5rDqKXvtKsQK3w15IE0DBNSE_lhxI'
CHAT_ID = '419777955'
API_URL = 'https://alif.tj/api/rates/history?currency=rub&date='


# Можно сохранить предыдущее значение в файл или базе
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
    telegram_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    try:
        requests.get(telegram_url, params=payload).raise_for_status()
    except Exception as e:
        print(f"[!] Ошибка при отправке Telegram-сообщения: {e}")

def main():
    rate = get_rub_rate()
    if rate is not None:
        with open("last_rate.txt", "r+") as f:
            try:
                prev_rate = float(f.read())
            except:
                prev_rate = None
            if prev_rate is None or rate != prev_rate:
                send_telegram_message(f"📢 Курс RUB изменился: {prev_rate} → {rate}")
                f.seek(0)
                f.write(str(rate))
                f.truncate()
    else:
        print("[-] Не удалось получить курс RUB.")

if __name__ == "__main__":
    main()
