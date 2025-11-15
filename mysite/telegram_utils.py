# telegram_utils.py
import requests
from django.conf import settings
from decouple import config


def send_application_to_telegram(application):
    """
    Отправляет заявку в Telegram бота через sendMessage API
    """
    # Получаем токен бота из настроек (пользователь должен добавить TELEGRAM_BOT_TOKEN в .env)
    telegram_bot_token = config('TELEGRAM_BOT_TOKEN', default='')
    telegram_chat_id = config('TELEGRAM_CHAT_ID', default='-1002626172514')
    
    if not telegram_bot_token:
        print("TELEGRAM_BOT_TOKEN не установлен в настройках")
        return
    
    text = (
        f"📥 Новая заявка с сайта:\n\n"
        f"👤 Имя: {application.name}\n"
        f"📞 Телефон: {application.phone}\n"
        f"📧 Email: {application.email}\n"
        f"🕐 Дата: {application.created_at.strftime('%d.%m.%Y %H:%M')}"
    )
    
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        'chat_id': telegram_chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке в Telegram: {e}")


# Оставляем старую функцию для обратной совместимости
def send_to_telegram(contact):
    """
    Старая функция для обратной совместимости
    """
    telegram_bot_token = config('TELEGRAM_BOT_TOKEN', default='')
    telegram_chat_id = config('TELEGRAM_CHAT_ID', default='-1002626172514')
    
    if not telegram_bot_token:
        print("TELEGRAM_BOT_TOKEN не установлен в настройках")
        return
    
    text = f"📥 Новая заявка с сайта:\n\n👤 Имя: {contact.name}\n📞 Телефон: {contact.phone}\n📧 Email: {contact.email}"
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        'chat_id': telegram_chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")
