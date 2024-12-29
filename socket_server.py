import socket
import json
from datetime import datetime
from pymongo import MongoClient

HOST = '0.0.0.0'
PORT = 5000

client = MongoClient('mongodb://mongo:27017/')
db = client['messages_db']
collection = db['messages']

def handle_client(conn):
    data = conn.recv(1024).decode('utf-8')
    message = json.loads(data)
    message['date'] = str(datetime.now())
    collection.insert_one(message)
    print(f"Message saved: {message}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Socket Server running on {HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            handle_client(conn)
            conn.close()

if __name__ == "__main__":
    main()
