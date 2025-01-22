import requests
import json

def main():
    lines = []
    
    print("Running...")

    # Read input file line by line
    with open("ollama_batch_api_input.jsonl", "r") as input_file:
        for line in input_file:
            # Parse each line as JSON
            payload = json.loads(line.strip())
            
            # Make API request with the payload
            r = requests.post('http://localhost:11434/api/generate', json=payload)
            
            # Store the response
            response = r.json()
            lines.append(json.dumps(response) + "\n")
            
            # Optional: Print progress
            print(f"Processed request: {payload.get('prompt', '')[:50]}...")

    # Write all responses to output file
    with open("ollama_batch_api_output.jsonl", "a") as write_file:
        write_file.writelines(lines)
    
    print("Done")

main()