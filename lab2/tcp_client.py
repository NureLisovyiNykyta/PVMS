import socket

HOST = '127.0.0.1'
PORT = 8001


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print("Connected to the TCP server.")

        a = input("Enter the first number: ")
        b = input("Enter the second number: ")

        message = f"{a},{b}"
        client_socket.send(message.encode('utf-8'))

        result = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {result}")

    except ConnectionRefusedError:
        print("Error: Connection refused. Is the server running?")
    finally:
        client_socket.close()


if __name__ == "__main__":
    run_client()