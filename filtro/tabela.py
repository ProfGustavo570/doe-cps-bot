from dataclasses import dataclass

BASE = '#ContentPlaceHolderConteudoPrincipal_ConteudoPrincipal_'


@dataclass
class Formulario:
    input_filtro:       str
    cell_edital:        str
    cell_escola:        str
    cell_area:          str
    cell_inicio:        str

formulario = Formulario(
    input_filtro    = f'{BASE}txtFiltro',
    cell_edital     = 'table  > tbody > tr > td:nth-child(6)',
    cell_escola     = 'table  > tbody > tr > td:nth-child(4)',
    cell_area       = 'table  > tbody > tr > td:nth-child(9)',
    cell_inicio     = 'table  > tbody > tr > td:nth-child(7)'
)
