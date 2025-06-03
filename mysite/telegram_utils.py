# telegram_utils.py
import requests
from django.conf import settings
from decouple import config


TELEGRAM_BOT_TOKEN = config('BOT_TOKEN')
TELEGRAM_CHAT_ID = '-1002626172514'

def send_to_telegram(contact):
    text = f"📥 Новая заявка с сайта:\n\n👤 Имя: {contact.name}\n📞 Телефон: {contact.phone}\n📧 Email: {contact.email}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")
