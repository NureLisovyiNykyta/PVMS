import socket
import time

HOST = '127.0.0.1'
PORT = 8002

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP Server running on {HOST}:{PORT}. Waiting for data...")

try:
    while True:
        data, client_address = server_socket.recvfrom(1024)
        # time.sleep(0.01)
        decoded_data = data.decode('utf-8')

        try:
            a, b = map(float, decoded_data.split(','))
            result = a + b
            response = f"Sum: {result}"
            print(f"[{client_address}] Received: {decoded_data}. Sending: {response}")
        except ValueError:
            response = "Error: Please send two numbers separated by a comma."

        server_socket.sendto(response.encode('utf-8'), client_address)
except KeyboardInterrupt:
    print("\nServer stopped.")
finally:
    server_socket.close()