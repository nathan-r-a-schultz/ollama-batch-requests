import requests

def main():
    payload = {"model": "llama3.3:70b", "prompt": "This is a test prompt. Please confirm you are working by saying 'Hello World!'", "stream": False}
    r = requests.post('http://localhost:11434/api/generate', json=payload)
    print(r.text)
    print("test")

main()