import urllib.request
import json
import traceback

def test_url(url):
    print(f"Testing {url} ...")
    req = urllib.request.Request(url, data=b'{"session_id": "test", "message": "test", "context": {}}', headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req)
        print("Success!", response.read().decode())
    except Exception as e:
        print("Error:", e)

test_url("http://127.0.0.1:8000/api/chat")
test_url("http://localhost:8000/api/chat")
