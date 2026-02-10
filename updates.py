import logging
import requests


class Updates:
    def get_updates(token):
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates"
            logging.info(requests.get(url).json())
        except Exception as error:
            logging.critical(error)


def send_no_publication(id, date):
    message = f'📭 <b>SEM PUBLICAÇÃO NO DIÁRIO OFICIAL</b>\n\nNão foram encontradas publicações em {date}\n\n<i>Mais atualizações amanhã!</i>'
    url = f"https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/sendMessage?chat_id={id}&parse_mode=html&text={message}"
    requests.get(url).json()


def send_updates(id, updated):
    message = f'{updated}\n\n<i>Mais atualizações amanhã!</i>'
    url = f"https://api.telegram.org/bot{os.getenv('BOT-TOKEN')}/sendMessage?chat_id={id}&parse_mode=html&text={message}"
    requests.get(url).json()


def scrap_routine(person, id):
    try:
        driver = init_driver()
        today = datetime.today().strftime('%d/%m/%Y')

        if has_publication(driver):
            message = f'🎯 <b>EDITAIS COM ATUALIZAÇÃO EM {today}</b>'

            spreadsheet = pandas.read_csv(
                f'./editais.csv',
                dtype=str
            )

            for index, row in spreadsheet.iterrows():
                process_edicts(driver, row)
                if row["ULTIMA AT"] == today:
                    message += f'''\n<b>{row['EDITAL']}</b> | <i>{row['MATERIA']}</i>'''

            if message.find('|') == -1:
                message = f'⏳ <b>EDITAIS SEM ATUALIZAÇÃO EM {today}</b>\n\n<i>Não houveram atualizações nos editais cadastrados :(</i>'

            spreadsheet.to_csv(f'./editais-{person.lower()}.csv', index=False)
            send_updates(id, message)

        else:
            send_no_publication(id, today)

        logging.info(f'{person.upper()}: OK')

    except Exception as error:
        logging.critical(f'{person.upper()}: {error}')

    finally:
        driver.quit()


load_dotenv()
Updates.get_updates(os.getenv('BOT-TOKEN'))
scrap_routine('gustavo', os.getenv('ID-GUSTAVO'))
scrap_routine('ana', os.getenv('ID-ANA'))
