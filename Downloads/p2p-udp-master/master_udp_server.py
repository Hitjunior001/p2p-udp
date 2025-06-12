import socket
import json
import threading
import base64
import os

broadcast_myip = '10.62.219.14'
broadcast_port = 50005
tcp_master_port = 50020

udpBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
udpBroadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udpBroadcast.bind((broadcast_myip, broadcast_port))

tasks_dir = "tasks"
results_dir = "results"


task_zip_path = os.path.join(tasks_dir, "example.zip")

if(os.path.exists(task_zip_path)):
    with open(task_zip_path, "rb") as f:
        task_zip_b64 = base64.b64encode(f.read()).decode()

print("waiting DISCOVER_MASTER...\n")

def receiveMessagePeer(data, addr):
    try:
        msg = json.loads(data.decode())
        if msg.get("action") == "DISCOVER_MASTER" and addr[0] != broadcast_myip:
            print(f"received DISCOVER_MASTER from {addr}")
            response = {
                "action": "MASTER_ANNOUNCE",
                "master_ip": broadcast_myip,
                "master_port": tcp_master_port
            }
            udpBroadcast.sendto(json.dumps(response).encode(), addr)
    except Exception as e:
        print(f"error from {addr}: {e}")

def handle_peer_connection(conn, addr):
    try:
        while True:
            data = conn.recv(65536)  
            if not data:
                break
            msg = json.loads(data.decode())

            action = msg.get("action")
            if action == "REGISTER":
                print(f"REGISTER from {msg['peer_id']} at {msg['addr']}")
                response = {"status": "REGISTERED"}
                conn.sendall(json.dumps(response).encode())

            elif action == "HEARTBEAT":
                print(f"HEARTBEAT from {msg['peer_id']}")
                response = {"status": "ALIVE"}
                conn.sendall(json.dumps(response).encode())

            elif action == "REQUEST_TASK":
                print(f"REQUEST_TASK from {msg['peer_id']}")
                response = {
                    "action": "TASK_PACKAGE",
                    "task_name": "example.zip",
                    "task_data": task_zip_b64
                }
                conn.sendall(json.dumps(response).encode())
                print(f"Sent TASK_PACKAGE to {msg['peer_id']}")

            elif action == "SUBMIT_RESULT":
                print(f"SUBMIT_RESULT from {msg['peer_id']} result: {msg['result_name']}")

                result_data_b64 = msg["result_data"]
                result_bytes = base64.b64decode(result_data_b64)
                result_file_path = os.path.join(results_dir, msg["result_name"])
                with open(result_file_path, "wb") as f:
                    f.write(result_bytes)
                print(f"Saved result to {result_file_path}")

                response = {"status": "OK"}
                conn.sendall(json.dumps(response).encode())

            else:
                print(f"err: {action}")

    except Exception as e:
        print(f"TCP error: {e}")
    finally:
        conn.close()

def start_tcp_master():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((broadcast_myip, tcp_master_port))
    server.listen()

    print(f"TCP listening on {broadcast_myip}:{tcp_master_port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_peer_connection, args=(conn, addr), daemon=True).start()

threading.Thread(target=start_tcp_master, daemon=True).start()

while True:
    try:
        data, addr = udpBroadcast.recvfrom(1024)
        threading.Thread(target=receiveMessagePeer, args=(data, addr)).start()
    except Exception as e:
        print(f"error: {e}")
