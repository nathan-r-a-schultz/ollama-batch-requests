import requests
import json
from tqdm import tqdm

def jsonl(inputFile, outputFile, MODEL):
    
    print("[%s][JSONL] Running..." % (MODEL))

    # Count total lines in input file first for the progress bar
    with open("src/" + inputFile, "r") as input_file:
        total_lines = sum(1 for _ in input_file)

    # Read input file line by line
    with open("src/" + inputFile, "r") as input_file:
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
            with open("src/" + outputFile, "a") as write_file:
                write_file.write(json.dumps(response) + "\n")
    
    print("Done")

def txt(inputFile, outputFile, MODEL):
    print("[%s][TXT] Running..." % (MODEL))

    # Count total lines in input file first for the progress bar
    with open("src/" + inputFile, "r") as input_file:
        total_lines = sum(1 for _ in input_file)

    # Read input file line by line
    with open("src/" + inputFile, "r") as input_file:
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
            payload = {
                "model": MODEL,
                "prompt": line.strip()
            }
            
            # Make API request with the payload
            r = requests.post('http://localhost:11434/api/generate', json=payload)
            
            # Get the response and save it immediately
            full_response = r.text
            try:
                # Parse each line of the response separately
                responses = [json.loads(resp) for resp in full_response.strip().split('\n')]
                response = responses[-1]  # Take the last response
            except json.JSONDecodeError:
                # Fallback to standard parsing if splitting fails
                response = r.json()

            with open("src/" + outputFile, "a") as write_file:
                write_file.write(json.dumps({
                    "input": line.strip(),
                    "response": response["response"]
                }) + "\n")
    
    print("Done")

def main():
    
    inputFile = "input.txt"
    outputFile = "output.txt"

    # inputFile = "input.jsonl"
    # outputFile = "output.jsonl"

    MODEL = "deepseek-r1:1.5b"

    if (inputFile.endswith(".jsonl")):
        jsonl(inputFile, outputFile, MODEL)
    elif(inputFile.endswith(".txt")):
        txt(inputFile, outputFile, MODEL)
    else:
        print("Invalid file format. Use jsonl or txt. Operation aborted.")


main()
