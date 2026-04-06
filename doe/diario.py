from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

import doe.telegram as telegram


def init_driver():
    options: Options = ChromeOptions()
    options.add_argument('-headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def processar_editais(driver, dados) -> str:
    driver.get('https://www.doe.sp.gov.br/busca-avancada')

    input_pesquisa = '.css-brmobe > input:nth-child(1)'
    txt_entrada = '.css-8atqhb > div:nth-child(3)'
    btn_pesquisar = 'button.MuiButton-root:nth-child(1)'

    driver.find_element(By.CSS_SELECTOR, input_pesquisa).send_keys(f'{dados[0]}')
    driver.find_element(By.CSS_SELECTOR, btn_pesquisar).click()
    
    if driver.find_elements(By.CSS_SELECTOR, txt_entrada):
        abas_antes = driver.window_handles
        driver.find_element(By.CSS_SELECTOR, txt_entrada).click()
        nova_aba = list(set(driver.window_handles) - set(abas_antes))[0]
        driver.switch_to.window(nova_aba)
        return f'\n<code>{dados[0]}</code> <code>({dados[2]})</code>  |  <a href="{driver.current_url}"><i>{dados[3]}</i></a>'
    else:
        return ''


def realizar_pesquisa(id) -> None:
    driver = init_driver()
    hoje: str = datetime.today().strftime('%d/%m/%Y')

    menssagem: str = f'🎯 <b>EDITAIS COM ATUALIZAÇÃO EM {hoje}</b>'

    with open(f'./doe/editais.csv', encoding='utf8', mode='r') as arquivo:
        editais: list[str] = arquivo.readlines()
        editais = editais[1:]

    for linha in editais:
        linha: str = linha.replace('\n','')
        dados: list[str] = linha.split(',')
        menssagem += processar_editais(driver, dados)
        print(f'{dados[0]}: OK')


    if menssagem.find('|') == -1:
        menssagem = f'⏳ <b>EDITAIS SEM ATUALIZAÇÃO EM {hoje}</b>\n\n<i>Não houveram atualizações nos editais cadastrados :(</i>'

    telegram.enviar_updates(id, menssagem)
