import os
import logging
import requests

def get_updates(token):
        try:
            url = f'https://api.telegram.org/bot{token}/getUpdates'
            logging.info(requests.get(url).json())
        except Exception as error:
            logging.critical(error)


def send_no_publication(id, date):
    message = f'📭 <b>SEM PUBLICAÇÃO NO DIÁRIO OFICIAL</b>\n\nNão foram encontradas publicações em {date}\n\n<i>Mais atualizações amanhã!</i>'
    url = f'https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/sendMessage?chat_id={id}&parse_mode=html&text={message}'
    requests.get(url).json()


def send_updates(id, updated):
    message = f'{updated}\n\n<i>Mais atualizações amanhã!</i>'
    url = f'https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/sendMessage?chat_id={id}&parse_mode=html&text={message}'
    requests.get(url).json()


