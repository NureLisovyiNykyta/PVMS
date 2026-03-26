import socket
import concurrent.futures
import time

HOST = '127.0.0.1'
PORT = 8001
CONNECTIONS = 1000


def make_broken_request(i):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((HOST, PORT))

        time.sleep(5)

        s.close()
        return True
    except Exception as e:
        return False


print(f"Starting concurrency test: {CONNECTIONS} blocked connections...")
start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    results = list(executor.map(make_broken_request, range(CONNECTIONS)))

end_time = time.time()

success = results.count(True)
errors = results.count(False)

print("--- Results ---")
print(f"Connections established: {success}")
print(f"Connections rejected: {errors}")