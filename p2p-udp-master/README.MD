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

/tasks # ZIPs de tarefas a serem distribuídas
/results # ZIPs de resultados processados
/work # Diretório temporário para extração e execução

---

## 🧪 Requisitos

- Python 3.7 ou superior  
- Criar previamente os diretórios: `tasks`, `results`, `work`  

---

## ⚙️ Instruções de Uso

### 🧭 `master_udp_server.py`

Peer TCP (Master) que responde a solicitações de descoberta e mantém conexões TCP com os peers.


