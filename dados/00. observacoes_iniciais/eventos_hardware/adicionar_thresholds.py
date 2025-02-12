import pandas as pd

# Caminho do arquivo consolidado
file_path = "/home/andre/projetos/dados/eventos_hardware/metricas_consolidadas.csv"

# Ler o arquivo consolidado
df = pd.read_csv(file_path)

# Definir thresholds específicos para cada microsserviço
thresholds = {
    "coturn": {"cpu": 20, "network": 1000000, "rps": None},
    "dialog": {"cpu": 20, "network": 1000000, "rps": None},
    "haproxy": {"cpu": 20, "network": 1000000, "rps": None},
    "hubs": {"cpu": 20, "network": 1000000, "rps": None},
    "nearspark": {"cpu": 20, "network": 1000000, "rps": None},
    "pgbouncer": {"cpu": 20, "network": 1000000, "rps": None},
    "pgbouncer-t": {"cpu": 20, "network": 1000000, "rps": None},
    "pgsql": {"cpu": 20, "network": 1000000, "rps": None},
    "photomnemonic": {"cpu": 20, "network": 1000000, "rps": None},
    "reticulum": {"cpu": 60, "network": None, "rps": 200},
    "spoke": {"cpu": 20, "network": 1000000, "rps": None},
}

# Adicionar colunas de thresholds para cada microsserviço
for service, values in thresholds.items():
    # Threshold de CPU
    if values["cpu"] is not None:
        df[f"{service}_cpu_threshold"] = values["cpu"]
    # Threshold de Rede
    if values["network"] is not None:
        df[f"{service}_network_threshold"] = values["network"]
    # Threshold de RPS
    if values["rps"] is not None:
        df[f"{service}_rps_threshold"] = values["rps"]

# Salvar o arquivo atualizado
output_file = "/home/andre/projetos/dados/eventos_hardware/metricas_consolidadas_com_thresholds.csv"
df.to_csv(output_file, index=False)
print(f"Arquivo atualizado com thresholds salvo em: {output_file}")
