<div align="center">

# Ollama Batch Requesting Tool

A Python script for efficiently processing batch requests to a local Ollama instance.

![GitHub license](https://img.shields.io/github/license/nathan-r-a-schultz/ollama-batch-requests)

</div>

## Overview

The Ollama Batch Requesting Tool is a command-line tool that enables batch processing of prompts to a local Ollama instance. It supports both JSONL and TXT file formats for input, with configurable model selection and response handling. The batch inputs are based on [OpenAI's batch API](https://platform.openai.com/docs/guides/batch) and [Ollama's /generate endpoint](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion) documentation.

## Features

- **Batch Processing**: Process multiple requests sequentially with progress tracking
- **Multiple Input Formats**: 
  - JSONL format for detailed request configuration
  - TXT format for simple prompt-based requests
- **Model Override**: Option to override model settings for batch requests
- **Single Request Mode**: Test individual prompts with optional system messages
- **Automatic Response Saving**: Save responses in JSONL or TXT format

## Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/ollama-batch-requests.git
cd ollama-batch-requests
```


2. Install dependencies
```bash
pip install requests tqdm
```

3. Ensure you have Ollama running locally on port 11434

## Usage

### Running the Script

```bash
python src/main.py
```

### Input File Formats

#### JSONL Object Format
```json
{"custom_id": "chat-1", "model": "llama2", "system": "You are a helpful assistant.", "prompt": "How are you?", "stream": false}
```

#### TXT Format
```text
Your prompt here
Another prompt here
```

### Output

Responses are saved to either:
- `src/data/output.jsonl` for JSONL format
- `src/data/output.txt` for TXT format

## Configuration

The script connects to Ollama at `http://localhost:11434` by default. Ensure your Ollama instance is running and accessible at this address.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Nathan Schultz
- Kay Roye

