import socket
import threading

clients = []
client_addresses = []

def accept_connections(server_socket):
    while True:
        try:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            client_addresses.append(addr)
        except Exception as e:
            print(f"Error accepting connections: {e}")
            break

def send_message_to_client(client_socket, message):
    try:
        client_socket.send(message.encode())
        response = client_socket.recv(4096).decode()
        print(f"\nResponse from {client_socket.getpeername()}:")
        print(response)
    except Exception as e:
        print(f"Error sending message: {e}")

def send_message_to_all(message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode())
            response = client_socket.recv(4096).decode()
            print(f"\nResponse from {client_socket.getpeername()}:")
            print(response)
        except Exception as e:
            print(f"Error sending message to {client_socket.getpeername()}: {e}")

def server_menu():
    while True:
        print("\n--- Server Menu ---")
        print("1. Send message to a specific client")
        print("2. Send message to all clients")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            if not clients:
                print("No clients connected.")
                continue
            print("Connected clients:")
            for idx, addr in enumerate(client_addresses):
                print(f"{idx}: {addr}")
            try:
                client_index = int(input("Enter client index: ").strip())
                if client_index < 0 or client_index >= len(clients):
                    print("Invalid client index.")
                    continue
                message = input("Enter message to send (or 'exit' to terminate communication): ")
                send_message_to_client(clients[client_index], message)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == "2":
            if not clients:
                print("No clients connected.")
                continue
            message = input("Enter message to send to all clients (or 'exit' to terminate communication): ")
            send_message_to_all(message)
        elif choice == "3":
            print("Exiting server menu and closing all connections.")
            for client_socket in clients:
                try:
                    client_socket.send("exit".encode())
                    client_socket.close()
                except:
                    pass
            break
        else:
            print("Invalid choice. Please try again.")

def start_server(ip='172.17.42.153', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Server listening on {ip}:{port}")

    threading.Thread(target=accept_connections, args=(server_socket,), daemon=True).start()

    server_menu()

    server_socket.close()

if __name__ == '__main__':
    start_server()
