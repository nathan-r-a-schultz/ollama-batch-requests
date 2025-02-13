import requests
import json
from tqdm import tqdm
from requests.exceptions import RequestException


def jsonl(inputFile, outputFile, MODEL, modelOverride):

    print("[JSONL] Running...")

    try:
        # Count total lines in input file first for the progress bar
        with open(inputFile, "r") as input_file:
            total_lines = sum(1 for _ in input_file)
            # Get the first line of the input file
            input_file.seek(0)
            first_line = json.loads(input_file.readline())
            # Set the model to the model specified in the first line of the input file if there is no model override
            try:
                if (modelOverride == 2):
                    MODEL = first_line['model']
            except json.JSONDecodeError:
                print("Invalid JSON object in the input file.")
                return

        with open(inputFile, "r") as input_file:
            # Initialize the model loading it into memory first with a test prompt
            payload = {
                "model": MODEL,
                "prompt": f"You are {MODEL}. You are about to be hit with some batch requests. Respond with your model name and if you are ready to handle the requests.",
                "stream": False,
            }
            try:
                # Request the Ollama API
                initResponse = requests.post(
                    'http://localhost:11434/api/generate', json=payload, timeout=30)
                # Raise an exception for bad status codes
                initResponse.raise_for_status()
                # Print the response
                print(initResponse.json()['response'])
                print("Model initialized, processing requests...")
            except RequestException as e:
                if (e.response.status_code == 404):
                    print(
                        f"Model \"{MODEL}\" not found on this Ollama instance, please check the model name and try again.")
                    return
                else:
                    print(f"Error initializing model: {e}")
                    return

            for line in tqdm(input_file, total=total_lines, desc="Processing requests"):
                try:
                    # Parse the line as JSON
                    payload = json.loads(line.strip())
                    # If there is a model override, set the model to the model specified by the user
                    if (modelOverride == 1):
                        payload["model"] = MODEL

                    r = requests.post(
                        'http://localhost:11434/api/generate', json=payload, timeout=30)
                    r.raise_for_status()
                    response = r.json()

                    # Immediately write the response to the output file
                    with open(outputFile, "a") as write_file:
                        write_file.write(json.dumps(response) + "\n")
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON line: {e}")
                    continue
                except RequestException as e:
                    print(f"Error making API request: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    continue
    except FileNotFoundError:
        print(f"Input file not found: {inputFile}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print(f"{total_lines} {'requests' if total_lines != 1 else 'request'} completed successfully.")

def txt(inputFile, outputFile, MODEL):
    print("[%s][TXT] Running..." % (MODEL))

    # Count total lines in input file first for the progress bar
    with open(inputFile, "r") as input_file:
        total_lines = sum(1 for line in input_file if line.strip())

    # Read input file line by line
    with open(inputFile, "r") as input_file:
        # Initialize the model, storing it in memory first
        payload = {
            "model": MODEL,
            "prompt": f"You are {MODEL}. You are about to be hit with some batch requests. Respond with your model name and if you are ready to handle the requests.",
            "stream": False,
        }
        initResponse = requests.post(
            'http://localhost:11434/api/generate', json=payload)
        print(initResponse.json()['response'])
        print("Model initialized, processing requests...")

        # Add progress bar
        for line in tqdm(input_file, total=total_lines, desc="Processing requests"):
            if line.strip() == "":
                continue
            # Parse each line as JSON
            payload = {
                "model": MODEL,
                "prompt": line.strip(),
                "stream": False
            }

            # Make API request with the payload
            r = requests.post(
                'http://localhost:11434/api/generate', json=payload)
            response = r.json()

            with open(outputFile, "a") as write_file:
                write_file.write(json.dumps({
                    "input": line.strip(),
                    "response": response['response']
                }) + "\n")

    print(f"{total_lines} {'requests' if total_lines != 1 else 'request'} completed successfully.")
