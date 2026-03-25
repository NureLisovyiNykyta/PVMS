import socket

HOST = '127.0.0.1'
PORT = 8001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(100)
print(f"TCP Server running on {HOST}:{PORT}. Waiting for connections...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[{client_address}] Connected")

        data = client_socket.recv(1024).decode('utf-8')

        if data:
            try:
                a, b = map(float, data.split(','))
                result = a + b
                response = f"Sum: {result}"
                print(f"[{client_address}] Received: {data}. Sending: {response}")
            except ValueError:
                response = "Error: Please send two numbers separated by a comma."

            client_socket.send(response.encode('utf-8'))

        client_socket.close()
except KeyboardInterrupt:
    print("\nServer stopped.")
finally:
    server_socket.close()