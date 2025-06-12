Projeto P2P - UDP

Intregantes:
- Rafael 
- Reginaldo
- Bruna
- Luiza

Tecnologias usada:
- Python (Linguagem)
- Socket (Conexão)
- Threading (Uso de threads)
- Json (Messagem via JSON)
- Base64 (Codificação para bytes)
- Zipfile (Criação e Leitura de arquivos zip)

Requisitos:
- Python 3.7 or > instalado
- Diretórios("tasks", "results", "work")

Instrução de uso:

```
master_udp_server.py 
- Peer que irá responder a solicitação de qualquer um na rede que envie "DISCOVER_MASTER" na porta especificada

Irá responder as seguintes mensagems através de ACTION enviado dentro de um JSON.
- "DISCOVER_MASTER":
{
 "action": "MASTER_ANNOUNCE",
 "master_ip": "<ip-master>",
 "master_port": <porta_tcp_master>
}
- "REGISTER":
{
    "status": "REGISTERED" 
}
- "HEARTBEAT":
{
     "status": "ALIVE" 
}


peer_udp_client.py
- Peer que irá enviar uma mensagem para todos na rede broadcast com a porta 
INPUTS:
- "DISCOVER_MASTER" -> Irá enviar uma mensagem para todos conectados na rede com o seguinte JSON
{
 "action": "DISCOVER_MASTER",
 "peer_id": "<uuid-peer>",
 "port_tcp": <porta_escuta_peer>
}
- "REGISTER" -> Irá criar uma conexão TCP com quem respondeu a mensagem "DISCOVER_MASTER" enviando a seguinte mensagem em JSON
{
 "action": "REGISTER",
 "peer_id": "<uuid-peer>",
 "addr": ["<ip-peer>",<porta_escuta_peer>]
}

- "HEARTBEAT" -> Irá enviar um sinal para o TCP (Master) com quem criou a conexão com a seguinte mensagem em JSON
{
 "action": "HEARTBEAT",
 "peer_id": "<uuid-peer>"
}
```

