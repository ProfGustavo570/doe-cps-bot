import os
import logging
from datetime import datetime

import pandas
# import requests
# from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

logging.basicConfig(
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()],
    encoding='utf-8',
    format='%(asctime)s [%(levelname)s: %(filename)s (line %(lineno)d)] %(message)s',
    datefmt='%d/%m/%Y - %H:%M:%S',
    level=logging.INFO
)


def init_driver():
    if os.path.exists('/usr/bin/firefox'):
        options = FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(10)
    else:
        options = ChromeOptions()
        options.binary_location = os.getenv('CHROME-PATH')
        options.add_argument('-headless')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)

    return driver


def process_edicts(driver, row, message):
    driver.get('https://www.doe.sp.gov.br/')

    input_search = '#search-input'
    btn_search = 'button.MuiButtonBase-root:nth-child(2)'
    txt_entry = '.css-8atqhb > div:nth-child(3)'

    driver.find_element(By.CSS_SELECTOR, input_search).send_keys(
        f'{row['EDITAL']}')
    driver.find_element(By.CSS_SELECTOR, btn_search).click()

    if driver.find_elements(By.CSS_SELECTOR, txt_entry):
        abas_antes = driver.window_handles
        driver.find_element(By.CSS_SELECTOR, txt_entry).click()
        wait.until(lambda d: len(d.window_handles) > len(abas_antes))
        nova_aba = list(set(driver.window_handles) - set(abas_antes))[0]
        driver.switch_to.window(nova_aba)
        row['ULTIMA AT'] = datetime.today().strftime('%d/%m/%Y')
        row['LINK'] = driver.current_url
        return f'{row['EDITAL']}\n'
    else:
        return ''


try:
    spreadsheet = pandas.read_csv(
        f'./editais.csv',
        dtype=str
    )
    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    message = 'EDITAIS COM ATUALIZAÇÕES\n'

    for index, row in spreadsheet.iterrows():
        message += process_edicts(driver, row, message)

    if message != 'EDITAIS COM ATUALIZAÇÕES\n':
        print(message.strip())
    else:
        print('Não houveram atualizações nos editais cadastrados.')

    spreadsheet.to_csv(f'./editais.csv', index=False)
    driver.quit()    

except Exception as e:
    driver.quit()
    logging.error(e)
