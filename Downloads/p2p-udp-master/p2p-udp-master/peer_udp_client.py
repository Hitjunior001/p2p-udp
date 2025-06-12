import socket
import threading
import json
import uuid
import time
import os
import base64
import zipfile
import subprocess

broadcast_port = 50005
peer_id = str(uuid.uuid4())
peer_tcp_port = 50010

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", peer_tcp_port))

master_info = {}
tcp_sock = None  

# Service Discovery (Master ↔ Peer) 
def receive_message():
    while True:
        try:
            data, addr = client.recvfrom(1024)
            msg = json.loads(data.decode())
            if msg.get("action") == "MASTER_ANNOUNCE":
                print(f'\n"action": "MASTER_ANNOUNCE"\n"master_ip": "{msg["master_ip"]}"\n"master_port": "{msg["master_port"]}"\n')
                master_info["ip"] = msg["master_ip"]
                master_info["port"] = int(msg["master_port"])

                threading.Thread(target=start_tcp_connection_to_master, daemon=True).start()
        except Exception as e:
            print(f"receive err: {e}")

# Registro (TCP Master ↔ Peer) 
def start_tcp_connection_to_master():
    global tcp_sock
    try:
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((master_info["ip"], master_info["port"]))

        register_msg = {
            "action": "REGISTER",
            "peer_id": peer_id,
            "addr": [socket.gethostbyname(socket.gethostname()), peer_tcp_port]
        }
        tcp_sock.sendall(json.dumps(register_msg).encode())
        print("Sending REGISTER")

        response = tcp_sock.recv(1024)
        print("Master response:", response.decode())

        #Ativando thread de loop após uma conexão com o TCP (Master) para enviar status de vivo
        threading.Thread(target=send_heartbeat_loop, daemon=True).start()

    except Exception as e:
        print("TCP error:", e)

# Heartbeat (TCP Master ↔ Peer) 
def send_heartbeat_loop():
    while True:
        heartbeat_msg = {
            "action": "HEARTBEAT",
            "peer_id": peer_id
        }
        try:
            #Ativando thread para enviar status de vivo para a conexão TCP (Master)
            tcp_sock.sendall(json.dumps(heartbeat_msg).encode())
            response = tcp_sock.recv(1024)
            print("Heartbeat:", response.decode())
        except Exception as e:
            print("Heartbeat error:", e)
            break
        time.sleep(5)

# Distribuição e Execução de Tarefas (Master ↔ Peer)
def request_and_execute_task():
    try:
        request_msg = {
            "action": "REQUEST_TASK",
            "peer_id": peer_id
        }
        tcp_sock.sendall(json.dumps(request_msg).encode())
        print("sent: REQUEST_TASK")

        response = tcp_sock.recv(1024)
        msg = json.loads(response.decode())
        if msg.get("action") == "TASK_PACKAGE":
            task_name = msg["task_name"]
            task_data_b64 = msg["task_data"]
            print(f"Received TASK_PACKAGE: {task_name}")

            os.makedirs("work", exist_ok=True)
            task_path = os.path.join("work", task_name)
            os.makedirs(task_path, exist_ok=True)

            zip_bytes = base64.b64decode(task_data_b64)
            zip_path = os.path.join(task_path, task_name)
            with open(zip_path, "wb") as f:
                f.write(zip_bytes)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(task_path)

            try:
                print("Executing main.py...")
                result = subprocess.run(
                    ["py", "main.py"],
                    cwd=task_path,
                    stdout=open(os.path.join(task_path, "stdout.txt"), "w"),
                    stderr=open(os.path.join(task_path, "stderr.txt"), "w")
                )
                print("Execution finished.")
            except Exception as e:
                print("Error:", e)

            result_zip_path = os.path.join("work", f"{task_name}_result.zip")
            with zipfile.ZipFile(result_zip_path, "w") as zipf:
                zipf.write(os.path.join(task_path, "stdout.txt"), arcname="stdout.txt")
                zipf.write(os.path.join(task_path, "stderr.txt"), arcname="stderr.txt")

            with open(result_zip_path, "rb") as f:
                result_data_b64 = base64.b64encode(f.read()).decode()

            submit_msg = {
                "action": "SUBMIT_RESULT",
                "peer_id": peer_id,
                "result_name": f"{task_name}_result.zip",
                "result_data": result_data_b64
            }

            tcp_sock.sendall(json.dumps(submit_msg).encode())
            response = tcp_sock.recv(1024)
            print("Result:", response.decode())

    except Exception as e:
        print("request err:", e)

#Ativando thread para receber mensagem UDP.
threading.Thread(target=receive_message, daemon=True).start()

print("Terminal:")
while True:
    cmd = input("[1] DISCOVER_MASTER | [2] REQUEST_TASK → EXECUTE: ").strip()
    if cmd == "1":
        try:
            message = {
                "action": "DISCOVER_MASTER",
                "peer_id": peer_id,
                "port_tcp": peer_tcp_port
            }
            
            client.sendto(json.dumps(message).encode(), ("10.62.219.255", broadcast_port))
            # client.sendto(json.dumps(message).encode(), ("<broadcast>", broadcast_port))
            print("Sent: DISCOVER_MASTER")
        except Exception as e:
            print(f"send err: {e}")
    elif cmd == "2":
        if tcp_sock:
            request_and_execute_task()
        else:
            print("Not connected.")
    else:
        print("Use [1] to discover or [2] to request task.")
