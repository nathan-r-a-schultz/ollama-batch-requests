import requests
import json

def main():
    lines = []

    print("Running...")

    # json goes in the payload
    payload = {}
    r = requests.post('http://localhost:11434/api/generate', json=payload)

    # printing the output works but saving it to a file doesn't
    print(r.json())
    lines.append(json.dumps(r.json()) + "\n")

    with open ("src/test_output.jsonl", "a") as writeFile:
        writeFile.writelines(lines)
        
        
    print("Done")


        
main()