import pandas as pd
import os

# Caminho do diretório onde os arquivos estão
directory = "."  # Substitua pelo caminho correto

# Nomes exatos das colunas fornecidas
column_names = [
    "timestamp", "01_requisicoes_por_segundo", "02_latencia", "03_tempo_resposta",
    "04_percentual_de_sucesso_das_requisicoes", "05_escalabilidade_reticulum",
    "06_escalabilidade_dialog", "07_escalabilidade_haproxy", "08_escalabilidade_coturn",
    "09_escalabilidade_hubs", "10_escalabilidade_nearspark", "11_escalabilidade_pgbouncer",
    "12_escalabilidade_pgbouncer-t", "13_escalabilidade_pgsql", "14_escalabilidade_spoke",
    "15_escalabilidade_photomnemonic", "16_percentual_cpu_cluster", "17_percentual_cpu_node1",
    "18_percentual_cpu_node2", "19_percentual_cpu_node3", "20_cpu_coturn", "21_cpu_dialog",
    "22_cpu_haproxy", "23_cpu_hubs", "24_cpu_nearspark", "25_cpu_pgbouncer", "26_cpu_pgbouncer-t",
    "27_cpu_pgsql", "28_cpu_photomnemonic", "29_cpu_reticulum", "30_cpu_spoke",
    "31_memoria_ativa_cluster", "32_total_memoria_ativa_node1", "33_total_memoria_ativa_node2",
    "34_total_memoria_ativa_node3", "35_percentual_memoria_node1", "36_percentual_memoria_node2",
    "37_percentual_memoria_node3", "38_total_memoria_reticulum", "39_total_memoria_dialog",
    "40_total_memoria_coturn", "41_total_memoria_haproxy", "42_total_memoria_hubs",
    "43_total_memoria_nearspark", "44_total_memoria_pgbouncer", "45_total_memoria_pgbouncer-t",
    "46_total_memoria_pgsql", "47_total_memoria_photomnemonic", "48_total_memoria_spoke",
    "49_percentual_memoria_reticulum", "50_percentual_memoria_coturn", "51_percentual_memoria_haproxy",
    "52_percentual_memoria_dialog", "53_percentual_memoria_hubs", "54_percentual_memoria_nearspark",
    "55_percentual_memoria_pgbouncer", "56_percentual_memoria_pgbouncer-t", "57_percentual_memoria_spoke",
    "58_percentual_memoria_pgsql", "59_percentual_memoria_photomnemonic", "60_transmissao_dados_cluster",
    "61_transmissao_dados_coturn", "62_transmissao_dados_dialog", "63_transmissao_dados_haproxy",
    "64_transmissao_dados_hubs", "65_transmissao_dados_nearspark", "66_transmissao_dados_pgbouncer",
    "67_transmissao_dados_pgsql", "68_transmissao_dados_photomnemonic", "69_transmissao_dados_reticulum",
    "70_transmissao_dados_spoke", "71_trasmissao_dados_pgbouncer-t"
]

# Lista para armazenar os DataFrames
dataframes = []

# Ler os arquivos CSV do diretório
for file in sorted(os.listdir(directory)):
    if file.endswith(".csv"):
        file_path = os.path.join(directory, file)
        print(f"Lendo arquivo: {file_path}")
        
        # Ler o arquivo ignorando a primeira linha e renomeando as colunas
        df = pd.read_csv(file_path, header=None, names=column_names, skiprows=1)
        
        # Converter a coluna 'timestamp' para datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Adicionar o DataFrame à lista
        dataframes.append(df)

# Concatenar os DataFrames e ordenar cronologicamente pelo timestamp
print("Sincronizando os arquivos...")
merged_df = pd.concat(dataframes, ignore_index=True)
merged_df.sort_values(by="timestamp", inplace=True)
merged_df.reset_index(drop=True, inplace=True)

# Salvar o resultado consolidado
output_file = os.path.join(directory, "evento_hardware.csv")
merged_df.to_csv(output_file, index=False)

print(f"Arquivo consolidado salvo em: {output_file}")
