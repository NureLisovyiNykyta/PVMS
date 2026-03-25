import socket

HOST = '127.0.0.1'
PORT = 8002


def run_udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2)

    try:
        a = input("Enter the first number: ")
        b = input("Enter the second number: ")

        message = f"{a},{b}"
        client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
        print("Data sent to the UDP server.")

        result, server_address = client_socket.recvfrom(1024)
        print(f"Server response: {result.decode('utf-8')}")

    except socket.timeout:
        print("Error: Request timed out. UDP doesn't guarantee delivery.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    run_udp_client()