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

if __name__ == "__main__":
    main()
