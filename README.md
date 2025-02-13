# Arquitetura de Dimensionamento Adaptativo e Inteligente para Aplicações Imersivas

Este repositório disponibiliza os conjuntos de dados obtidos a partir da avaliação experimental de estratégias de escalonamento para a aplicação Hubs VR. A pesquisa analisou o impacto da utilização de métricas de hardware e eventos da aplicação no dimensionamento automático dos microsserviços, utilizando tecnologias como Kubernetes, KEDA, Prometheus e Grafana.  

Os dados coletados permitem avaliar a eficácia dessas abordagens e servirão de referência para a modelagem de uma arquitetura de escalonamento adaptativo e inteligente, buscando maior estabilidade e eficiência na alocação de recursos em aplicações imersivas.  

---

## 1. Conjuntos de Dados Disponíveis  

Os dados coletados nos experimentos foram organizados em dois conjuntos distintos, conforme a abordagem adotada para o escalonamento:  

### Estratégia baseada apenas em métricas de hardware  
- Considera apenas uso de CPU e tráfego de rede como parâmetros para escalonamento.  

### Estratégia baseada em métricas combinadas (hardware e eventos da aplicação)  
- Utiliza uso de CPU, tráfego de rede e taxa de requisições por segundo.  

Os arquivos de dados podem ser encontrados na pasta `dados/` deste repositório.  

---

## 2. Tecnologias Utilizadas  

Os experimentos foram conduzidos utilizando as seguintes tecnologias:  

- **[Kubernetes (K8s)](https://kubernetes.io/)** → Orquestração dos microsserviços da aplicação Hubs VR.  
- **[KEDA](https://keda.sh/)** → Escalonamento dinâmico baseado em eventos da aplicação.  
- **[Prometheus](https://prometheus.io/)** → Monitoramento e coleta de métricas do sistema.  
- **[Grafana](https://grafana.com/)** → Visualização e análise gráfica das métricas coletadas.  
- **[k6](https://k6.io/)** → Testes de carga para simulação de usuários e análise do comportamento do sistema.  
- **[Hubs Cloud](https://github.com/Hubs-Foundation/hubs-cloud/tree/master/community-edition)** → Execução da aplicação Hubs em ambiente controlado.  

Essas ferramentas permitiram a coleta estruturada de métricas, possibilitando a análise comparativa entre as abordagens de escalonamento.  

---

## 3. Metodologia e Caso de Uso  

O objetivo dos experimentos foi avaliar o comportamento da aplicação Hubs VR diante de diferentes estratégias de escalonamento. A configuração experimental incluiu:  

### Fluxo Experimental  
1. Simulação de diferentes cargas de usuários utilizando [k6](https://k6.io/), variando de 55 a 700 conexões simultâneas.  
2. Coleta de métricas em tempo real via [Prometheus](https://prometheus.io/) e [Grafana](https://grafana.com/).  
3. Comparação do desempenho do sistema sob duas abordagens de escalonamento:  
   - Apenas métricas de hardware.  
   - Métricas combinadas (hardware e eventos da aplicação).  
4. Análise dos impactos nas seguintes métricas:  
   - Requisições por segundo.  
   - Latência.  
   - Tempo de resposta.  
   - Percentual de sucesso das requisições.  

Os dados gerados neste estudo servirão de referência para a modelagem de uma arquitetura de escalonamento mais eficiente para a aplicação Hubs VR.  

---

## 4. Resultados e Análises  

Os dados coletados permitiram a comparação entre os dois cenários, destacando os seguintes aspectos:  

- Maior estabilidade no escalonamento com métricas combinadas.  
- Redução no tempo de resposta e latência quando eventos da aplicação são incorporados.  
- Menor dispersão e maior previsibilidade do comportamento do sistema sob carga variável.  
- Aprimoramento da alocação de recursos, reduzindo consumo desnecessário de memória.  

Essas observações reforçam a importância de associar métricas de hardware com eventos da aplicação para obter ajustes mais rápidos e precisos no escalonamento de microsserviços.  
