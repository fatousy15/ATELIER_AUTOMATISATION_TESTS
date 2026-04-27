import requests
import time

BASE_URL = "https://api.agify.io"
TIMEOUT = 3

def get(endpoint, params=None, retry=1):
    url = BASE_URL + endpoint
    for attempt in range(retry + 1):
        try:
            start = time.time()
            response = requests.get(url, params=params, timeout=TIMEOUT)
            latency = (time.time() - start) * 1000
            if response.status_code == 429:
                time.sleep(2)
                continue
            return response, round(latency, 2)
        except requests.exceptions.Timeout:
            if attempt == retry:
                raise
            time.sleep(1)
