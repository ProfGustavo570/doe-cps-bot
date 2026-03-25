from datetime import datetime

import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

import doe.telegram as telegram


def init_driver():
    options = ChromeOptions()
    options.add_argument('-headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def processar_editais(driver, row):
    driver.get('https://www.doe.sp.gov.br/busca-avancada')

    input_pesquisa = '.css-brmobe > input:nth-child(1)'
    txt_entrada = '.css-8atqhb > div:nth-child(3)'
    btn_pesquisar = 'button.MuiButton-root:nth-child(1)'

    driver.find_element(By.CSS_SELECTOR, input_pesquisa).send_keys(f'{row['EDITAL']}')
    driver.find_element(By.CSS_SELECTOR, btn_pesquisar).click()

    print(f'{row['EDITAL']}: OK')
    
    if driver.find_elements(By.CSS_SELECTOR, txt_entrada):
        abas_antes = driver.window_handles
        driver.find_element(By.CSS_SELECTOR, txt_entrada).click()
        nova_aba = list(set(driver.window_handles) - set(abas_antes))[0]
        driver.switch_to.window(nova_aba)
        return f'\n<code>{row['EDITAL']}</code> <code>({row['TIPO']})</code>  |  <a href="{driver.current_url}"><i>{row['MATERIA']}</i></a>'
    else:
        return ''


def realizar_pesquisa(id):
    driver = init_driver()
    hoje = datetime.today().strftime('%d/%m/%Y')

    menssagem = f'🎯 <b>EDITAIS COM ATUALIZAÇÃO EM {hoje}</b>'

    editais = pandas.read_csv(
        f'./doe/editais.csv',
        delimiter=',',
        dtype=str
    )

    for index, row in editais.iterrows():
        menssagem += processar_editais(driver, row)

    if menssagem.find('|') == -1:
        menssagem = f'⏳ <b>EDITAIS SEM ATUALIZAÇÃO EM {hoje}</b>\n\n<i>Não houveram atualizações nos editais cadastrados :(</i>'

    telegram.enviar_updates(id, menssagem)
