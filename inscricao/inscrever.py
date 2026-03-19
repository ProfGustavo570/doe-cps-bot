import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


from inscricao import candidato, formulario


def init_driver():
    if os.path.exists('/usr/bin/firefox'):
        options = FirefoxOptions()
        # options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(10)
    else:
        options = ChromeOptions()
        # options.add_argument('-headless')
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


def inscrever_pss(edital):
    driver = init_driver()
    dados = candidato.candidato
    pss = formulario.pss

    driver.get(
        'https://urhsistemas.cps.sp.gov.br/dgsdad/selecaopublica/ETEC/PSS/Abertos.aspx'
    )
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # Filtro e seleção do edital
    preencher(driver, pss.input_filtro, edital)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    clicar(driver, pss.botao_filtro)

    # ESC para fechar possível modal
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    clicar(driver, pss.botao_inscrever)

    # CPF
    preencher(driver, pss.input_cpf, dados.cpf)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(1)
    preencher(driver, pss.input_reptcpf, dados.cpf)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()

    # Dados pessoais
    preencher(driver, pss.input_nome, dados.nome)
    clicar(driver, pss.radio_trans)
    preencher(driver, pss.input_nasc, dados.nascimento)
    preencher(driver, pss.input_rg, dados.rg)
    clicar(driver, pss.radio_masc)

    # Contato
    preencher(driver, pss.input_email, dados.email)
    preencher(driver, pss.input_altemail, dados.email)
    preencher(driver, pss.input_ddd, dados.ddd)
    preencher(driver, pss.input_fone, dados.fone)

    # Estado civil (Select)
    Select(css(driver, pss.input_civil)).select_by_index(1)

    # Endereço
    preencher(driver, pss.input_cep, dados.cep)
    # time.sleep(2)  # aguarda autopreenchimento do CEP, se houver
    preencher(driver, pss.input_rua, dados.rua)
    preencher(driver, pss.input_numero, dados.numero)
    preencher(driver, pss.input_bairro, dados.bairro)
    preencher(driver, pss.input_cidade, dados.cidade)
    preencher(driver, pss.input_estado, dados.estado)

    # Informações adicionais
    clicar(driver, pss.radio_jurado)
    clicar(driver, pss.radio_cadunico)
    clicar(driver, pss.radio_pcd)
    clicar(driver, pss.botao_pessoal)

    # Raça
    Select(css(driver, pss.select_raca)).select_by_index(1)
    clicar(driver, pss.botao_raca)

    # Tipo de inscrição
    Select(css(driver, pss.select_grad)).select_by_index(2)
    clicar(driver, pss.botao_grad)

    # Upload do memorial
    css(driver, pss.input_memo).send_keys(os.path.abspath('./inscricao/Memorial.pdf'))
    clicar(driver, pss.botao_memo)
    time.sleep(3)

    # Confirmações
    clicar(driver, pss.check_1)
    clicar(driver, pss.check_2)
    clicar(driver, pss.check_3)
    clicar(driver, pss.check_4)

    # Submeter
    clicar(driver, pss.botao_confirmar)
    time.sleep(5)

    driver.quit()
