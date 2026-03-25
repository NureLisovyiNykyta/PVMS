import requests
import concurrent.futures
import time

URL = "http://127.0.0.1:8000/String?value=(test_load)"
CONNECTIONS = 10000

def make_request(i):
    try:
        response = requests.get(URL, timeout=5)
        return response.status_code
    except Exception as e:
        return "Error/Timeout"

print(f"Starting stress test: {CONNECTIONS} concurrent connections...")
start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    results = list(executor.map(make_request, range(CONNECTIONS)))

end_time = time.time()

success = results.count(200)
errors = len(results) - success

print(f"--- Results ---")
print(f"Successful requests (200 OK): {success}")
print(f"Errors / Timeouts: {errors}")
print(f"Execution time: {round(end_time - start_time, 2)} sec.")