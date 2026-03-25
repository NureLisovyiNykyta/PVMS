import socket
import concurrent.futures
import time

HOST = '127.0.0.1'
PORT = 8001
CONNECTIONS = 100000

def make_tcp_request(i):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, PORT))
        s.send(b"5,7")
        response = s.recv(1024)
        s.close()
        return True
    except Exception:
        return False

print(f"Starting TCP stress test: {CONNECTIONS} concurrent connections...")
start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    results = list(executor.map(make_tcp_request, range(CONNECTIONS)))

end_time = time.time()

success = results.count(True)
errors = results.count(False)

print("--- Results ---")
print(f"Successful connections: {success}")
print(f"Failed connections / Timeouts: {errors}")
print(f"Execution time: {round(end_time - start_time, 2)} sec.")