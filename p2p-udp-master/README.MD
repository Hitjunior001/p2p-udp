Projeto P2P Escalável  
**Disciplina:** Sistemas Distribuídos  
**Professor:** Prof. Me. Michel Junio  

## 👥 Integrantes
- Rafael  
- Reginaldo  
- Bruna  
- Luiza  

---

## 🎯 Objetivo

Desenvolver um sistema peer-to-peer (P2P) com as seguintes características:

1. **Service Discovery:** Peers localizam automaticamente o Master via broadcast UDP.  
2. **Distribuição de Tarefas:** Master envia tarefas compactadas (ZIP) com scripts Python e arquivos CSV para execução pelos peers.  
3. **Execução Distribuída:** Peers executam os scripts localmente e retornam os resultados.  
4. **Interoperabilidade:** Comunicação padronizada entre peers e masters de diferentes grupos via JSON.

---

## 🛠️ Tecnologias Utilizadas

- **Python** – Linguagem principal  
- **Socket** – Comunicação em rede (UDP/TCP)  
- **Threading** – Execução concorrente  
- **JSON** – Protocolo de mensagens  
- **Base64** – Codificação de arquivos ZIP para envio  
- **Zipfile** – Manipulação de arquivos ZIP  

---

## 📁 Estrutura de Diretórios

**No Master:**
/tasks # ZIPs de tarefas a serem distribuídas
/results # ZIPs de resultados processados

**No Peer:**
/work # Diretório temporário para extração e execução

---

## 🧪 Requisitos

- Python 3.7 ou superior  
- Criar previamente os diretórios: `tasks`, `results`, `work`  

---

## ⚙️ Instruções de Uso

### 🧭 `master_udp_server.py`

Peer TCP (Master) que responde a solicitações de descoberta e mantém conexões TCP com os peers.

#### Mensagens UDP recebidas:
- **DISCOVER_MASTER**
```json
// Resposta:
{
  "action": "MASTER_ANNOUNCE",
  "master_ip": "<ip-do-master>",
  "master_port": <porta-tcp-master>
}
Mensagens TCP:
REGISTER


// Enviado pelo peer:
{
  "action": "REGISTER",
  "peer_id": "<uuid-peer>",
  "addr": ["<ip-peer>", <porta-escuta-peer>]
}
// Resposta do master:
{ "status": "REGISTERED" }
HEARTBEAT

// Enviado periodicamente pelo peer:
{
  "action": "HEARTBEAT",
  "peer_id": "<uuid-peer>"
}
// Resposta:
{ "status": "ALIVE" }
🌐 peer_udp_client.py
Peer que participa da rede e realiza o processo de descoberta, registro e execução de tarefas.

Ações disponíveis:
DISCOVER_MASTER – Envia broadcast UDP:

{
  "action": "DISCOVER_MASTER",
  "peer_id": "<uuid-peer>",
  "port_tcp": <porta_tcp_peer>
}
REGISTER – Estabelece conexão TCP com o Master:

{
  "action": "REGISTER",
  "peer_id": "<uuid-peer>",
  "addr": ["<ip-peer>", <porta_tcp_peer>]
}
HEARTBEAT – Mantém a conexão viva com o Master:

{
  "action": "HEARTBEAT",
  "peer_id": "<uuid-peer>"
}
📦 Execução e Processamento de Tarefas
Ciclo completo:
REQUEST_TASK – Peer solicita uma tarefa:

{
  "action": "REQUEST_TASK",
  "peer_id": "<uuid-peer>"
}
TASK_PACKAGE – Master envia a tarefa:

{
  "action": "TASK_PACKAGE",
  "task_name": "exemplo.zip",
  "task_data": "<base64-do-arquivo>"
}
Execução local no peer:
O ZIP é extraído em work/<task_name>/, onde main.py é executado sobre input.csv. Os arquivos stdout.txt e stderr.txt são gerados.

SUBMIT_RESULT – Peer envia os resultados ao Master:

{
  "action": "SUBMIT_RESULT",
  "peer_id": "<uuid-peer>",
  "result_name": "exemplo.zip",
  "result_data": "<base64-do-resultado>"
}
Confirmação do Master:

{ "status": "OK" }
