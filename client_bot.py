import socket
import subprocess

def start_client(ip='172.17.42.153', port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print(f"Connected to server at {ip}:{port}")

    while True:
        message = client.recv(4096).decode()

        if message.lower() == 'exit':
            print("Server has terminated the communication.")
            break

        print(f"Received message: {message}")

        if message.lower() == "open_explorer":
            try:
                subprocess.Popen("explorer")
                response = "File Explorer opened successfully."
            except Exception as e:
                response = f"Error opening File Explorer: {e}"
        else:
            response = f"Client received: {message}"
        client.send(response.encode())

    client.close()

if __name__ == '__main__':
    start_client()
