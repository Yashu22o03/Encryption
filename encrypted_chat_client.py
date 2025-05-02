import socket
import threading
from cryptography.fernet import Fernet
import os
import sys

#  Load the shared encryption key
try:
    with open("shared-key.key", "rb") as f:
        key = f.read()
except FileNotFoundError:
    print("ERROR: 'shared-key.key' not found. Run generate_key.py first.")
    sys.exit(1)

cipher = Fernet(key)

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to receive and decrypt messages
def receive_messages():
    while True:
        try:
            encrypted_msg = client.recv(1024)
            if encrypted_msg:
                print(f"\n[Encrypted Received]: {encrypted_msg.decode()}")
                decrypted_msg = cipher.decrypt(encrypted_msg).decode()
                print(f"[Decrypted Message]: {decrypted_msg}\nYou: ", end='')
        except:
            print(" Disconnected from server.")
            break

# Function to encrypt and send messages
def send_messages():
    while True:
        msg = input("You: ")
        encrypted_msg = cipher.encrypt(msg.encode())
        print(f"[Plaintext]: {msg}")
        print(f"[Encrypted Sent]: {encrypted_msg.decode()}")
        client.send(encrypted_msg)

# Start threads for sending and receiving
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()
