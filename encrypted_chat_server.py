import socket
import threading
from cryptography.fernet import Fernet
import os
import sys

# 🔐 Load the shared encryption key
try:
    with open("shared-key.key", "rb") as f:
        key = f.read()
except FileNotFoundError:
    print("ERROR: 'shared-key.key' not found. Run generate_key.py first.")
    sys.exit(1)

cipher = Fernet(key)

HOST = '127.0.0.1'  # Use 0.0.0.0 to listen on all interfaces
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def handle_client(client_socket):
    while True:
        try:
            encrypted_msg = client_socket.recv(1024)
            if not encrypted_msg:
                break

            # Log encrypted and decrypted messages
            print(f"\n [Encrypted Received]: {encrypted_msg.decode()}")
            decrypted = cipher.decrypt(encrypted_msg).decode()
            print(f"[Decrypted Message]: {decrypted}")

            broadcast(encrypted_msg, client_socket)

        except Exception as e:
            print(f"Client disconnected or error occurred: {e}")
            if client_socket in clients:
                clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, source_socket):
    for client in clients:
        if client != source_socket:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

print("Server is running and waiting for connections...")
while True:
    client_socket, addr = server.accept()
    print(f"✅ Connected: {addr}")
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
