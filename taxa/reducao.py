import io
import os
import smtplib

from pypdf import PdfReader, PdfWriter
from email.message import EmailMessage


def gerar_documento(edital) -> None:
    reader = PdfReader('./taxa/formulario_empty.pdf')
    writer = PdfWriter()
    merger = PdfWriter()
    buffer = io.BytesIO()

    writer.clone_reader_document_root(reader)

    writer.update_page_form_field_values(
        writer.pages[0],
        {
            'edital_1': edital,
            'edital_2': edital
        },
    )

    writer.write(buffer)

    documentos: list[BytesIO | str] = [
        buffer,
        './taxa/declaracao.pdf',
        './taxa/desempregado.pdf',
        './taxa/ctps.pdf'
    ]

    for documento in documentos:
        merger.append(documento)

    with open(f'./taxa/documentacao/{edital.replace('/', '-')}.pdf', 'wb') as file:
        merger.write(file)


def enviar_mensagem(edital, email) -> None:
    gerar_documento(edital)
    
    menssagem: str = f'''
    Olá, espero que esta mensagem os encontre bem.
    <br><br>
    Venho por meio deste e-mail realizar a solicitação para redução da taxa de inscrição do edital <b>{edital}</b>.
    <br><br>
    Segue em anexo o arquivo contendo:
    <ol>
    <li>Formulário de solicitação;</li>
    <li>Declaração de matrícula (Estácio);</li>
    <li>Declaração de situação de desemprego;</li>
    <li>Carteira de trabalho digital com último contrato em 30/01/2026.</li>
    </ol>
    Agradeço desde já pela atenção e me coloco a disposição em caso de eventuais problemas com a solicitação.
    <br><br>
    Atenciosamente,
    <br>
    Prof. Gustavo Sergio Fernandes
    '''

    msg = EmailMessage()
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    msg['Subject'] = f'SOLICITAÇÃO DE REDUÇÃO/ISENÇÃO DA TAXA DE INSCRIÇÃO – CONCURSO PÚBLICO DOCENTE EDITAL Nº {edital}'
    msg['From'] = 'Gustavo Fernandes (Prof Gustavo)'
    msg['To'] = email
    msg.set_content(menssagem, subtype='html')
    with open(f'./taxa/documentacao/{edital.replace('/', '-')}.pdf', 'rb') as file:
        msg.add_attachment(
            file.read(),
            maintype='application',
            subtype='pdf',
            filename=f'{edital.replace('/', '-')}_documentacao.pdf'
        )

    smtp.login(os.getenv('SENDER-MAIL'), os.getenv('SENDER-PSWD'))
    smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
