import os
import requests


def get_updates():
    url = f'https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/getUpdates'
    print(requests.get(url).json())


def enviar_updates(id, updated):
    message = f'{updated}\n\n<i>Mais atualizações amanhã!</i>'
    url = f'https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/sendMessage'
    params = {
        'chat_id': id,
        'parse_mode': 'HTML',
        'text': message,
        'disable_web_page_preview': True
    }
    requests.get(url, params=params).json()
