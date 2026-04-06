import os
import requests


def get_updates() -> None:
    url: str = f'https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/getUpdates'
    print(requests.get(url).json())


def enviar_updates(id, updated) -> None:
    message: str = f'{updated}\n\n<i>Mais atualizações amanhã!</i>'
    url: str = f'https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/sendMessage'
    params: dict[str, bool | str | Unknown] = {
        'chat_id': id,
        'parse_mode': 'HTML',
        'text': message,
        'disable_web_page_preview': True
    }
    requests.get(url, params=params).json()
