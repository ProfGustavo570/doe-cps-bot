import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


from .candidato import dados as candidato
from .formulario import campos


def init_driver():
    driver = webdriver.Chrome()
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


def realizar_inscricao(edital, tipo):
    driver = init_driver()
    dados = candidato
    form = campos

    driver.get(
        f'https://urhsistemas.cps.sp.gov.br/dgsdad/selecaopublica/ETEC/{tipo}/Abertos.aspx'
    )
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # Filtro e seleção do edital
    preencher(driver, form.input_filtro, edital)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    clicar(driver, form.botao_filtro)

    # ESC para fechar possível modal
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    clicar(driver, form.botao_inscrever)

    # CPF
    preencher(driver, form.input_cpf, dados.cpf)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(1)
    preencher(driver, form.input_reptcpf, dados.cpf)
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()

    # Dados pessoais
    preencher(driver, form.input_nome, dados.nome)
    clicar(driver, form.radio_trans)
    preencher(driver, form.input_nasc, dados.nascimento)
    preencher(driver, form.input_rg, dados.rg)
    clicar(driver, form.radio_masc)

    # Contato
    preencher(driver, form.input_email, dados.email)
    preencher(driver, form.input_altemail, dados.email)
    preencher(driver, form.input_ddd, dados.ddd)
    preencher(driver, form.input_fone, dados.fone)

    # Estado civil (Select)
    Select(css(driver, form.input_civil)).select_by_index(1)

    # Endereço
    preencher(driver, form.input_cep, dados.cep)
    # time.sleep(2)  # aguarda autopreenchimento do CEP, se houver
    preencher(driver, form.input_rua, dados.rua)
    preencher(driver, form.input_numero, dados.numero)
    preencher(driver, form.input_bairro, dados.bairro)
    preencher(driver, form.input_cidade, dados.cidade)
    preencher(driver, form.input_estado, dados.estado)

    # Informações adicionais
    clicar(driver, form.radio_jurado)
    clicar(driver, form.radio_cadunico)
    clicar(driver, form.radio_pcd)
    clicar(driver, form.botao_pessoal)

    # Raça
    Select(css(driver, form.select_raca)).select_by_index(1)
    clicar(driver, form.botao_raca)

    # Tipo de graduação
    Select(css(driver, form.select_grad)).select_by_index(2)
    clicar(driver, form.botao_grad)

    # Upload do memorial/taxa
    if tipo == 'PSS':
        css(driver, form.input_memo).send_keys(os.path.abspath('./inscricao/Memorial.pdf'))
        clicar(driver, form.botao_memo)
    else:
        css(driver, form.input_taxa).send_keys(os.path.abspath(f'./inscricao/comprovantes/{edital.replace('/', '-')}.pdf'))
        clicar(driver, form.botao_taxa)
    time.sleep(3)

    # Confirmações
    clicar(driver, form.check_1)
    clicar(driver, form.check_2)
    clicar(driver, form.check_3)
    clicar(driver, form.check_4)

    # Submeter
    clicar(driver, form.botao_confirmar)
    time.sleep(5)

    driver.quit()
