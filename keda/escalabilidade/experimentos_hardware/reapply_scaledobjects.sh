#!/bin/bash

# Defina o namespace onde os ScaledObjects estão
NAMESPACE="hcce"

# Diretório onde estão os arquivos YAML
YAML_DIR="./"

# Deleta todos os ScaledObjects no namespace especificado
echo "Deletando todos os ScaledObjects no namespace '$NAMESPACE'..."
kubectl delete scaledobject --all -n "$NAMESPACE"

# Lista os arquivos YAML no diretório e aplica-os novamente
echo "Aplicando os arquivos YAML para recriar os ScaledObjects..."
for file in "$YAML_DIR"*.yaml; do
  if [ -f "$file" ]; then
    echo "Aplicando $file..."
    kubectl apply -f "$file" -n "$NAMESPACE"
  else
    echo "Nenhum arquivo YAML encontrado em $YAML_DIR"
    exit 1
  fi
done

echo "Todos os ScaledObjects foram recriados com sucesso!"
