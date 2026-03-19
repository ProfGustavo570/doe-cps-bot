import os
from dotenv import load_dotenv

import doe.diario as diario
import inscricao.inscrever as inscrever
import taxa.reducao as reducao

load_dotenv()
inscrever.inscrever_pss(edital='')
diario.realizar_pesquisa(id=os.getenv('CHAT-ID'))
reducao.enviar_mensagem(edital='', email='')
