import requests
from request.start_batch import jsonl
from request.start_batch import txt

def main():
    print("Starting...")
    print("""
    ==================================================
    |                                                |
    |          Ollama Batch Request Tool             |
    |                                                |
    |        By: Nathan Schultz & Kay Roye           |
    |                                                |
    ==================================================
    
    1. Start Batch
    2. Run a single request
    3. Exit
    """)

    choice = int(input("Enter your choice: "))

    if choice == 1:
        model = ""
        inputLocation = "src/data/input."
        modelOverride = 2

        fileType = int(input("Enter the file type (1. JSONL, 2. TXT): "))
        inputLocation = input(
            "Enter the path to the input file (leave blank for default - data/input.*): ")

        # Set default location if none provided
        if inputLocation == "":
            inputLocation = "src/data/input.jsonl" if fileType == 1 else "src/data/input.txt"

        fileType = checkFileType(fileType, inputLocation)

        if fileType == 1:

            modelOverride = int(input(
                "Would you like to override the model used in each request? (1. Yes, 2. No): "))

            if modelOverride == 1:
                model = input("Enter the model to use: ")

            if inputLocation == "":
                inputLocation = "src/data/input.jsonl"

            jsonl(inputLocation, "src/data/output.jsonl", model, modelOverride)
        elif fileType == 2:
            model = input("Enter the model to use: ")
            txt(inputLocation, "src/data/output.txt", model)
    elif choice == 2:
        singleRequest()
    elif choice == 3:
        exit()

def checkFileType(fileType, inputLocation):
    if fileType == 1 and inputLocation.endswith(".jsonl"):
        return 1
    elif fileType == 2 and inputLocation.endswith(".txt"):
        return 2
    elif fileType == 1 and not inputLocation.endswith(".jsonl"):
        print("Invalid file type: Expected .jsonl file")
        exit()
    elif fileType == 2 and not inputLocation.endswith(".txt"):
        print("Invalid file type: Expected .txt file")
        exit()
    else:
        print("Invalid file type")
        exit()

def singleRequest():
    prompt = input("Enter the prompt to send: ")
    model = input("Enter the model to use: ")
    system_prompt = input("Enter the system prompt to use (blank for none): ")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    if system_prompt != "":
        payload["system"] = system_prompt

    r = requests.post("http://localhost:11434/api/generate", json=payload)
    print(r.json()['response'])

    while True:
        saveChoice = input("Would you like to save the response? (y/n): ")
        if saveChoice == "y":
            with open("src/data/output.txt", "a") as f:
                f.write(r.json()['response'] + "\n")
            break
        elif saveChoice == "n":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
