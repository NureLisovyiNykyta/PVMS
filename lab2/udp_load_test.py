import socket
import concurrent.futures
import time

HOST = '127.0.0.1'
PORT = 8002
REQUESTS = 500

def make_udp_request(i):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.sendto(b"5,7", (HOST, PORT))
        response, _ = s.recvfrom(1024)
        s.close()
        return True
    except socket.timeout:
        return False
    except Exception:
        return False

print(f"Starting UDP stress test: sending {REQUESTS} packets...")
start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=REQUESTS) as executor:
    results = list(executor.map(make_udp_request, range(REQUESTS)))

end_time = time.time()

success = results.count(True)
dropped = results.count(False)

print("--- Results ---")
print(f"Successful responses: {success}")
print(f"Dropped packets / Timeouts: {dropped}")
print(f"Execution time: {round(end_time - start_time, 2)} sec.")