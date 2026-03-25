import os
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options as ChromeOptions


from .tabela import formulario
import inscricao.inscrever as inscricao


def init_driver():
    options = ChromeOptions()
    options.add_argument('-headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


def css(driver, selector, wait=10, tentativas=3):
    for tentativa in range(tentativas):
        try:
            return WebDriverWait(driver, wait).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
        except StaleElementReferenceException:
            if tentativa == tentativas - 1:
                raise
            time.sleep(0.5)


def preencher(driver, selector, valor):
    for tentativa in range(3):
        try:
            elemento = css(driver, selector)
            elemento.send_keys(valor)
            time.sleep(0.5)
            return
        except StaleElementReferenceException:
            if tentativa == 2:
                raise
            time.sleep(0.5)


def clicar(driver, selector):
    for tentativa in range(3):
        try:
            css(driver, selector).click()
            time.sleep(0.5)
            return
        except StaleElementReferenceException:
            if tentativa == 2:
                raise
            time.sleep(0.5)


def filtrar_por_cidade(cidade, tipo):
    driver = init_driver()
    tabela = formulario

    driver.get(
        f'https://urhsistemas.cps.sp.gov.br/dgsdad/selecaopublica/ETEC/{tipo}/Abertos.aspx'
    )

    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    preencher(driver, tabela.input_filtro, cidade)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    
    cell_edital = driver.find_elements(By.CSS_SELECTOR, tabela.cell_edital)
    cell_escola = driver.find_elements(By.CSS_SELECTOR, tabela.cell_escola)
    cell_area = driver.find_elements(By.CSS_SELECTOR, tabela.cell_area)
    cell_inicio = driver.find_elements(By.CSS_SELECTOR, tabela.cell_inicio)
   

    for item in range(len(cell_edital)):
        materia = cell_area[item].text.split(' - ')

        with open(os.path.abspath('./filtro/crt.txt'), 'r') as crt:
            conteudo = crt.read()

        if materia[1].upper() in conteudo:
            message = ''
            
            if datetime.strptime(cell_inicio[item].text, '%d/%m/%y') < datetime.now():
                message += '[-- ABERTO --] '
            else:
                message += '[** FECHADO **] '
            
            message += cell_edital[item].text + ' - '
            message += cell_escola[item].text.replace('Escola Técnica Estadual', 'Etec') + ' | '
            message += materia[1]
        
            print(message)
            
            if 'ABERTO' in message:
                escolha = input('Deseja se inscrever neste edital (s/N): ')
                if escolha.upper().find('S') >= 0:
                    if tipo == 'PSS':
                        print(f'🗳️ Realizando inscrição no Processo Nº{cell_edital[item].text}...')
                    else:
                        print(f'🗳️ Realizando inscrição no Concurso Nº{cell_edital[item].text}...')
                    
                    inscricao.realizar_inscricao(cell_edital[item].text, tipo)
                    
                    print('✅ inscrição realizada com sucesso!')

    driver.quit()
