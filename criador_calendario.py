import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Dados de entrada
inicio = datetime(2023, 1, 1)
fim = datetime(2023, 12, 31)
feriados = ['2023-01-01', '2023-12-25']  # Adicione mais feriados conforme necessário
feriados = [datetime.strptime(date, '%Y-%m-%d') for date in feriados]

# Parâmetros
dias_empresa = 4
dias_capacitacao = 1

# Criar DataFrame de datas
datas = pd.date_range(start=inicio, end=fim)
calendario = pd.DataFrame(datas, columns=['Data'])
calendario['DiaSemana'] = calendario['Data'].dt.dayofweek
calendario['Atividade'] = 'Empresa'  # Default

# Marcar finais de semana
calendario.loc[calendario['DiaSemana'] >= 5, 'Atividade'] = 'Fim de Semana'

# Marcar feriados
calendario.loc[calendario['Data'].isin(feriados), 'Atividade'] = 'Feriado'

# Marcar dias de capacitação teórica
capacitacao_count = 0
for i in range(len(calendario)):
    if calendario.loc[i, 'Atividade'] == 'Empresa':
        capacitacao_count += 1
        if capacitacao_count % 5 == 0:
            calendario.loc[i, 'Atividade'] = 'Capacitacao'
            capacitacao_count = 0

# Exportar para CSV
calendario.to_csv('calendario_trabalho.csv', index=False)

# Exportar para XLSX com cores
import openpyxl
from openpyxl.styles import PatternFill

# Carregar o DataFrame para o Excel
calendario.to_excel('calendario_trabalho.xlsx', index=False)
wb = openpyxl.load_workbook('calendario_trabalho.xlsx')
ws = wb.active

# Definir cores
fill_empresa = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
fill_capacitacao = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
fill_feriado = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
fill_fim_semana = PatternFill(start_color="C0C0C0", end_color="C0C0C0", fill_type="solid")

# Aplicar cores
for row in ws.iter_rows(min_row=2, min_col=1, max_col=3):
    atividade = row[2].value
    if atividade == 'Empresa':
        fill = fill_empresa
    elif atividade == 'Capacitacao':
        fill = fill_capacitacao
    elif atividade == 'Feriado':
        fill = fill_feriado
    else:
        fill = fill_fim_semana
    for cell in row:
        cell.fill = fill

wb.save('calendario_trabalho.xlsx')
