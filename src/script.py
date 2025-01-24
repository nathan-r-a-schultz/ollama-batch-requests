import requests
import json
from tqdm import tqdm

def main():
    MODEL = "deepseek-r1:70b"
    
    print("Running...")

    # Count total lines in input file first for the progress bar
    with open("src/ollama_batch_api_input.jsonl", "r") as input_file:
        total_lines = sum(1 for _ in input_file)

    # Read input file line by line
    with open("src/ollama_batch_api_input.jsonl", "r") as input_file:
        # Initialize the model, storing it in memory first
        payload = {
            "model": MODEL,
            "prompt": f"You are {MODEL}. You are about to be hit with some batch requests. Respond with your model name and if you are ready to handle the requests.",
            "stream": False,
        }
        initResponse = requests.post('http://localhost:11434/api/generate', json=payload)
        print(initResponse.json()['response'])
        print("Model initialized, processing requests...")

        # Add progress bar
        for line in tqdm(input_file, total=total_lines, desc="Processing requests"):
            # Parse each line as JSON
            payload = json.loads(line.strip())
            payload['model'] = MODEL

            if "format" in payload:
                del payload["format"]
            
            # Make API request with the payload
            r = requests.post('http://localhost:11434/api/generate', json=payload)
            
            # Get the response and save it immediately
            response = r.json()
            response["response"] = response["response"].split("```json")[1].split("```")[0].strip()
            
            # Write response immediately to output file
            with open("src/ollama_batch_api_output.jsonl", "a") as write_file:
                write_file.write(json.dumps(response) + "\n")
    
    print("Done")

main()
