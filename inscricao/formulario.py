from dataclasses import dataclass

BASE = '#ContentPlaceHolderConteudoPrincipal_ConteudoPrincipal_'


@dataclass
class Formulario:
    input_filtro:        str
    botao_filtro:        str
    botao_inscrever:     str
    input_cpf:           str
    input_reptcpf:       str
    input_nome:          str
    radio_trans:         str
    input_nasc:          str
    input_rg:            str
    radio_masc:          str
    input_email:         str
    input_altemail:      str
    input_ddd:           str
    input_fone:          str
    input_civil:         str
    input_cep:           str
    input_rua:           str
    input_numero:        str
    input_bairro:        str
    input_cidade:        str
    input_estado:        str
    radio_jurado:        str
    radio_cadunico:      str
    radio_pcd:           str
    botao_pessoal:       str
    select_raca:         str
    botao_raca:          str
    select_grad:         str
    botao_grad:          str
    input_memo:          str
    botao_memo:          str
    input_taxa:          str
    botao_taxa:          str
    check_1:             str
    check_2:             str
    check_3:             str
    check_4:             str
    botao_confirmar:     str


pss = Formulario(
    input_filtro    = f'{BASE}txtFiltro',
    botao_filtro    = f'{BASE}GridViewPSSFATECFiltro > tbody > tr:nth-child(2) > td:nth-child(2) > a',
    botao_inscrever = f'{BASE}linkbtnInscricaoAberta',

    input_cpf       = f'{BASE}txtCPF',
    input_reptcpf   = f'{BASE}txtRcpf',

    input_nome      = f'{BASE}txtNome',
    radio_trans     = f'{BASE}rdbNomeSocial_1',
    input_nasc      = f'{BASE}txtDTNascimento',
    input_rg        = f'{BASE}txtRg',
    radio_masc      = f'{BASE}rdbSexo_0',

    input_email     = f'{BASE}txtEmail',
    input_altemail  = f'{BASE}txtEmailAlternativo',
    input_ddd       = f'{BASE}txtTelefoneDDD',
    input_fone      = f'{BASE}txtTelefone',

    input_civil     = f'{BASE}ddlEstadoCivil',
    
    input_cep       = f'{BASE}txtEnderecoCEP',
    input_rua       = f'{BASE}txtEndereco',
    input_numero    = f'{BASE}txtEnderecoNumero',
    input_bairro    = f'{BASE}txtEnderecoBairro',
    input_cidade    = f'{BASE}txtEnderecoCidade',
    input_estado    = f'{BASE}txtEnderecoEstado',

    radio_jurado    = f'{BASE}rdbJurado_1',
    radio_cadunico  = f'{BASE}rdbCadastroUnico_1',
    radio_pcd       = f'{BASE}rdbDeficienteSN > tbody > tr > td:nth-child(2)',
    botao_pessoal   = f'{BASE}bntInformacoesComplementares',

    select_raca     = f'{BASE}ddlPPICor',
    botao_raca      = f'{BASE}btnPontuacaoDiferenciadaSemFoto',

    select_grad     = f'{BASE}ddlTipoInscricao',
    botao_grad      = f'{BASE}btnRequisitos',

    input_memo      = f'{BASE}flpMemorialInscricao',
    botao_memo      = f'{BASE}btnSubirMemorial',

    input_taxa      = '',
    botao_taxa      = '',

    check_1         = f'{BASE}PanelConfirmacoes > div:nth-child(3) > span',
    check_2         = f'{BASE}chkCienteCondicoes',
    check_3         = f'{BASE}chkLGPD',
    check_4         = f'{BASE}chkResponsabilidade',

    botao_confirmar = f'{BASE}btnConfirmarInscricao',
)
