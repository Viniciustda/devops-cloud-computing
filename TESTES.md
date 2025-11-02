# Testes de Cliente para a API de Recomendação

Este projeto usa `curl` (um cliente CLI) para testar o endpoint da API.

## Teste de Recomendação Simples

Este comando envia um pedido de recomendação para a API. O `CLUSTER-IP` (neste exemplo, `10.43.41.11`) é obtido através do comando `kubectl -n viniciusabel get service tp2-api-service`.

```bash
curl -X POST http://10.43.41.11:50031/api/recommend \
-H "Content-Type: application/json" \
-d "{\"songs\": [\"Night's On Fire\"]}"
```

## Resposta

```bash
{"model_date":1762045011.8077958,"songs":["Crash And Burn"],"version":"2.1"}
```
`Obs.:` O model_date específico varia dependendo de quando o Job de ML correu.

## Teste de Monitorização Contínua (Usado na Parte 3)

Para medir o downtime (tempo de inatividade) durante as atualizações do ArgoCD, foi usado o seguinte loop de bash. Ele faz um pedido à API a cada segundo e imprime a resposta, permitindo observar atualizações de versão e modelo em tempo real.

```bash
# Define o IP do serviço numa variável
export API_IP=10.43.41.11

# Inicia o loop de monitorização
while true; do curl -X POST http://10.43.41.11:50031/api/recommend -H "Content-Type: application/json" -d '{"songs": ["Night'\''s On Fire"]}' --connect-timeout 1; echo ""; sleep 1; done
```