import pandas as pd
import os
import re

# Caminho para o diretório com os arquivos CSV
directory = "/home/andre/projetos/dados/analise4/eventos_hardware/metricas_capturadas"

# Lista para armazenar os DataFrames processados
dataframes = []

# Iterar sobre os arquivos no diretório
file_order = []
for file in os.listdir(directory):
    if file.endswith(".csv"):
        file_path = os.path.join(directory, file)
        # Ler o arquivo CSV
        df = pd.read_csv(file_path)
        # Extrair o nome da métrica do arquivo
        metric_name = os.path.splitext(file)[0]
        # Renomear a coluna 'value' para o nome da métrica correspondente
        df.rename(columns={"value": metric_name}, inplace=True)
        # Garantir que o timestamp seja tratado corretamente
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        # Adicionar o DataFrame processado à lista
        dataframes.append(df)
        # Registrar a ordem do arquivo para ordenar colunas posteriormente
        file_order.append(metric_name)

# Unir todos os DataFrames pelo timestamp
result_df = pd.DataFrame()
for df in dataframes:
    if result_df.empty:
        result_df = df
    else:
        # Merge com base no timestamp
        result_df = pd.merge(result_df, df, on="timestamp", how="outer")

# Ordenar pelo timestamp e redefinir o índice
result_df.sort_values(by="timestamp", inplace=True)
result_df.reset_index(drop=True, inplace=True)

# Reordenar colunas com base nos números extraídos dos nomes
def extract_number(column_name):
    """Função para extrair o número de um nome de coluna."""
    match = re.search(r'(\d+)', column_name)  # Procura por números
    return int(match.group(1)) if match else float('inf')  # Se não encontrar, coloca no final

# Reorganizar as colunas mantendo 'timestamp' no início
sorted_columns = ['timestamp'] + sorted(
    [col for col in result_df.columns if col != 'timestamp'],
    key=extract_number
)
result_df = result_df[sorted_columns]

# Salvar o resultado consolidado em um arquivo CSV
output_file = "/home/andre/projetos/dados/analise4/eventos_hardware/eventos_hardware_4.csv"
result_df.to_csv(output_file, index=False)
print(f"Dados consolidados salvos em: {output_file}")