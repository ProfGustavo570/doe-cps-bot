import os
import re
from time import sleep
import subprocess
from dotenv import load_dotenv

import doe.diario as diario
import inscricao.inscrever as inscrever
import taxa.reducao as reducao
import filtro.filtrar as filtrar

load_dotenv()
user = os.getenv('USER').upper()


def limpar_console() -> None:
    sleep(3)
    subprocess.run('cls' if os.name == 'nt' else 'clear')

def home_screen(escolha) -> None:    
    acao = ''
    
    match escolha:
        case 1 | 2 | 3:
            acao = 'Pesquisa'
        case 4 | 5:
            acao = 'Inscrição'
        case 6:
            acao = 'Solicitação'
    
    print(f'✅ {acao} realizada com sucesso!')
    sleep(3)
    print('Retornando à tela inicial...')
    sleep(3)
    limpar_console()


while True:
    print(f'Bem-vindo, {user}!\n{'='*30}\nO que deseja fazer hoje?\n{'-'*30}')
    print('1) Realizar consulta em editais cadastrados')
    print('2) Pesquisar por Processos Seletivos em uma região')
    print('3) Pesquisar por Concursos Públicos em uma região')
    print('4) Se inscrever em um Processo Seletivo')
    print('5) Se inscrever em um Concurso Público')
    print('6) Enviar um e-mail de redução de taxa')
    print('Ou digite outro número para encerrar a aplicação')
    escolha: str = input(f'{'-'*30}\nESCOLHA: ')

    if not escolha.isnumeric():
        limpar_console()
        print('Opção inválida, selecione novamente.')
    else:
        escolha = int(escolha)
        limpar_console()
        
        if escolha < 1 or escolha > 6:
            print(f'Até a próxima, {user}!')
            sleep(5)
            break

        elif escolha == 1:
            print('📰 Verificando o Diário Oficial...')
            diario.realizar_pesquisa(id=os.getenv('CHAT-ID'))
            home_screen(escolha)
        
        elif escolha <= 3:
            tipo = 'PSS' if escolha == 2 else 'CPD'
            cidade: str = input('Para prosseguir, digite o nome de uma cidade: ')

            print(f'🔍 Pesquisando na região de {cidade.upper()}...')
            filtrar.filtrar_por_cidade(cidade, tipo)
            home_screen(escolha)
            
        else:
            while True:
                edital: str = input('Para prosseguir, digite o número do edital (Ex: 000/00/0000): ')
                
                if bool(re.fullmatch(r'\d{3}/\d{2}/\d{4}', edital)):                   
                    if escolha == 4:
                        print(f'🗳️ Realizando inscrição no Processo Nº{edital}...')
                        inscrever.realizar_inscricao(edital=edital, tipo='PSS')
                        home_screen(escolha)
                        
                    elif escolha == 5:
                        print(f'🗳️ Realizando inscrição no Concurso Nº{edital}...')
                        inscrever.realizar_inscricao(edital=edital, tipo='CPD')
                        home_screen(escolha)
                        
                    else:
                        while True:
                            email: str = input('Digite o e-mail da escola que receberá a solicitação: ')
                            
                            if email.find('@') > 0:
                                print(f'📩 Enviando solicitação para {email} ({edital})...')
                                reducao.enviar_mensagem(edital=edital, email=email.strip())
                                home_screen(escolha)
                                break
                            else:
                                print('O email digitado é inválido, tente novamente.')
                                limpar_console()
                    break
                else:
                    print('O número digitado é inválido, tente novamente.')
                    limpar_console()

