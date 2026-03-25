import os
from dataclasses import dataclass


@dataclass
class Candidato:
    cpf:            str
    nome:           str
    nascimento:     str
    rg:             str
    email:          str
    ddd:            str
    fone:           str
    cep:            str
    rua:            str
    numero:         str
    bairro:         str
    cidade:         str
    estado:         str


dados = Candidato(
    cpf=os.getenv('cpf'),
    nome=os.getenv('nome'),
    nascimento=os.getenv('nascimento'),
    rg=os.getenv('rg'),
    email=os.getenv('email'),
    ddd=os.getenv('ddd'),
    fone=os.getenv('fone'),
    cep=os.getenv('cep'),
    rua=os.getenv('rua'),
    numero=os.getenv('numero'),
    bairro=os.getenv('bairro'),
    cidade=os.getenv('cidade'),
    estado=os.getenv('estado')
)
