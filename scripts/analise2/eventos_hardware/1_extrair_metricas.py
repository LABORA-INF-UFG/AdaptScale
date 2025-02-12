import os
import json
import requests
import pandas as pd

# URL do Prometheus
PROMETHEUS_URL = "http://127.0.0.1:9090/api/v1/query_range"

#Extração de dados - Gatilhos para escalar réplicas: Eventos+Hardware - Análise 4
# Data: 12 de dezembro de 2024 - Horário: 09:53:05 a 11:55:15
START="2024-12-12T09:53:05Z"
END="2024-12-12T11:55:15Z"
STEP = "5s"

# Lista de métricas que serão extraídas
metricas = [

  # 1. Quantidade de requisições por segundo
  'rate(k6_http_reqs_total[1m])',

  # 2. Latência das requisições HTTP
  'k6_http_req_duration_p99{method="GET", status="200", url="https://virtualhubs.online"}',

  # 3. Tempo de resposta
  'k6_http_req_waiting_p99{expected_response="true", name="https://virtualhubs.online"}',

  # 4. Percentual de sucesso das requisições
  'k6_checks_rate',

  # 5/15. Escalabilidade dos microsserviços
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"reticulum-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"dialog-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"haproxy-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"coturn-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"hubs-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"nearspark-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"pgbouncer-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"pgbouncer-t-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"pgsql-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"spoke-.*"})',
  'count(kube_pod_status_phase{namespace="hcce", phase="Running", pod=~"photomnemonic-.*"})',

  # 16. Percentual de uso de CPU no cluster
  '100 - (sum(rate(node_cpu_seconds_total{mode="idle"}[5m])) / sum(rate(node_cpu_seconds_total[5m])) * 100)',

  # 17/19. Utilização de CPU por nó
  '(sum(rate(node_cpu_seconds_total{mode!="idle", instance="10.116.0.2:9100"}[5m])) * 100) / sum(machine_cpu_cores{instance="virtualhubs2-wpncz"})',
  '(sum(rate(node_cpu_seconds_total{mode!="idle", instance="10.116.0.3:9100"}[5m])) * 100) / sum(machine_cpu_cores{instance="pool-7gp85uhw1-w0uco"})',
  '(sum(rate(node_cpu_seconds_total{mode!="idle", instance="10.116.0.4:9100"}[5m])) * 100) / sum(machine_cpu_cores{instance="pool-7gp85uhw1-w0ucx"})',

  # 20/30. Consumo de CPU por microsserviço
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"coturn-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"dialog-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"haproxy-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"hubs-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"nearspark-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"pgbouncer-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"pgbouncer-t.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"pgsql-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"photomnemonic-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"reticulum-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',
  'sum(rate(container_cpu_usage_seconds_total{namespace="hcce", pod=~"spoke-.*"}[5m])) * 100 / count(node_cpu_seconds_total{mode="idle"})',

  # 31. Total de memória ativa no cluster
  'sum(node_memory_Active_bytes)',

  # 32/34 Total de memória ativa por nó
  'node_memory_Active_bytes{node="virtualhubs2-wpncz", instance="10.116.0.2:9100"} / 1024 / 1024',
  'node_memory_Active_bytes{node="pool-7gp85uhw1-w0uco", instance="10.116.0.3:9100"} / 1024 / 1024',
  'node_memory_Active_bytes{node="pool-7gp85uhw1-w0ucx", instance="10.116.0.4:9100"} / 1024 / 1024',

  # 35/37. Percentual de memória ativa por nó
  '(node_memory_Active_bytes{instance="10.116.0.2:9100"} / node_memory_MemTotal_bytes{instance="10.116.0.2:9100"}) * 100',
  '(node_memory_Active_bytes{instance="10.116.0.3:9100"} * 100) / node_memory_MemTotal_bytes{instance="10.116.0.3:9100"}',
  '(node_memory_Active_bytes{instance="10.116.0.4:9100"} * 100) / node_memory_MemTotal_bytes{instance="10.116.0.4:9100"}',

  # 38/48 Consumo de memória por microsserviço
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"reticulum-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"dialog-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"coturn-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"haproxy-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"hubs-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"nearspark-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"pgbouncer-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"pgbouncer-t-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"pgsql-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"photomnemonic-.*"})',
  'sum(container_memory_usage_bytes{namespace="hcce", pod=~"spoke-.*"})',

  # 49/59. Percentual de memória ativa por microsserviço
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"reticulum-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"coturn-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"haproxy-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"dialog-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"hubs-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"nearspark-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"pgbouncer-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"pgbouncer-t.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"spoke-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"pgsql-.*"}) / sum(node_memory_Active_bytes)',
  '100 * sum(container_memory_usage_bytes{namespace="hcce", pod=~"photomnemonic-.*"}) / sum(node_memory_Active_bytes)',

   # 60 Taxa de transmissão de dados no cluster
   'sum(rate(container_network_receive_bytes_total[5m])) + sum(rate(container_network_transmit_bytes_total[5m]))',

   # 61/71 Taxa de transmissão de dados por microsserviços
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"coturn-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"coturn-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"dialog-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"dialog-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"haproxy-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"haproxy-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"hubs-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"hubs-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"nearspark-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"nearspark-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"pgbouncer-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"pgbouncer-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"pgsql-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"pgsql-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"photomnemonic-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"photomnemonic-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"reticulum-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"reticulum-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"spoke-.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"spoke-.*"}[5m]))',
   'sum(rate(container_network_transmit_bytes_total{namespace="hcce", pod=~"pgbouncer-t.*"}[5m])) + sum(rate(container_network_receive_bytes_total{namespace="hcce", pod=~"pgbouncer-t.*"}[5m]))', 
]

# Caminho para a pasta 'metricas_capturadas'
PASTA_METRICAS = os.path.join(os.path.dirname(__file__), "metricas_capturadas")

# Criar a pasta se não existir
os.makedirs(PASTA_METRICAS, exist_ok=True)

# Função para consultar o Prometheus
def consultar_prometheus(metrica):
    payload = {"query": metrica, "start": START, "end": END, "step": STEP}
    response = requests.get(PROMETHEUS_URL, params=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao consultar métrica '{metrica}': {response.status_code}")
        return None

# Loop para consultar cada métrica e salvar em arquivos separados
for i, metrica in enumerate(metricas, start=1):
    print(f"Consultando métrica: {metrica}")
    dados = consultar_prometheus(metrica)
    
    if dados and dados.get("status") == "success":
        resultados = dados["data"]["result"]
        dfs = []
        
        for resultado in resultados:
            valores = resultado["values"]
            df = pd.DataFrame(valores, columns=["timestamp", "value"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            dfs.append(df)
        
        # Concatenar DataFrames
        df_final = pd.concat(dfs, ignore_index=True)
        
        # Salvar na pasta 'metricas_capturadas'
        nome_arquivo = os.path.join(PASTA_METRICAS, f"metrica_{i}.csv")
        df_final.to_csv(nome_arquivo, index=False)
        print(f"Métrica '{metrica}' salva em: {nome_arquivo}")
    else:
        print(f"Erro ao processar métrica: {metrica}")
