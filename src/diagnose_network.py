import requests
import socket
import ssl
import sys

print(f"Python Version: {sys.version}")
print(f"Requests Version: {requests.__version__}")

URLS = [
    ("Ergast API (HTTP)", "http://ergast.com/api/f1/2024.json"),
    ("F1 Live Timing (HTTPS)", "https://livetiming.formula1.com/static/2024/2024-03-02_Bahrain_Grand_Prix/2024-03-02_Race/SessionInfo.json")
]

print("\n--- Network Diagnostic ---")

for name, url in URLS:
    print(f"\nTesting: {name}")
    print(f"URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('Content-Type', 'Unknown')}")
        if response.status_code == 200:
            print("SUCCESS: Data received.")
            print(f"Snippet: {response.text[:100]}...")
        else:
            print("FAILURE: Non-200 response.")
    except requests.exceptions.SSLError as e:
        print(f"CRITICAL SSL ERROR: {e}")
        print("Hint: This is common on Windows corporate/school networks or if root certs are missing.")
    except requests.exceptions.ConnectionError as e:
        print(f"CONNECTION ERROR: {e}")
    except Exception as e:
        print(f"UNKNOWN ERROR: {type(e).__name__}: {e}")

print("\n--- DNS Check ---")
try:
    ip = socket.gethostbyname("livetiming.formula1.com")
    print(f"livetiming.formula1.com resolved to: {ip}")
except Exception as e:
    print(f"DNS RESOLUTION FAILED: {e}")
