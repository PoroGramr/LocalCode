# Ollama Native Coding Agent (OA) 🚀

This project is a lightweight, high-performance coding agent that completely separates the **model server (e.g., Mac Studio)** from the **agent runner (Local Machine)**. It directly utilizes Ollama's native `/api/chat` (Tool Calling) API for seamless and efficient code interaction.

## ✨ Key Features
- **Ollama Native Tool Calling**: Directly uses Ollama 0.3+ tool calling capabilities without any additional compatibility layers.
- **Stateful Multi-turn**: Maintains conversation history to allow contextual code modifications and complex multi-step reasoning.
- **Server-Client Separation**: Decouples the heavy LLM inference from the agent logic, allowing for optimal resource utilization across your local network.
- **Interactive REPL**: Features a persistent command-line interface that allows you to chat and iterate on tasks continuously.

## 🛠 Installation (Global CLI Setup)

1. **Clone the repository and enter the directory**
   ```bash
   git clone <your-repo-url>
   cd LocalCode
   ```

2. **Install the package in Editable mode**
   This command registers the `oa` command globally on your system.
   ```bash
   pip install -e .
   ```

## 🚀 Usage

### Basic Execution
Open your terminal in any directory and run:
```bash
oa --host "http://[MAC-STUDIO-IP]:11434" --model "qwen3-coder:30b"
```

### Pro Tip: Setup an Alias
To avoid typing the host and model every time, add an alias to your `.zshrc` (or `.bashrc`):

```bash
# Add this to your ~/.zshrc file
alias codex='oa --host "http://192.168.1.100:11434" --model "llama3.1:8b"'
```
After saving, simply type `codex` in your terminal to summon your AI coding assistant.

## 🧰 Capabilities (Tools)
- `search_code`: Search for specific code patterns within the project.
- `read_file`: Read file contents with line numbers for context.
- `propose_patch`: Find a specific code block and apply precise modifications.
- `run_test`: Execute shell commands and run tests.
- `final`: Report task completion and provide a summary of changes.

## ⚠️ Important Notes
- **Ollama Version**: Recommended version 0.3.0 or higher.
- **Model Support**: Requires models that officially support Tool Calling (e.g., `llama3.1`, `mistral-nemo`, `qwen2.5-coder`).
- **Server Configuration**: Ensure the Ollama server on your Mac Studio allows external connections (`OLLAMA_HOST=0.0.0.0`).

---
*Since this agent can directly modify your source code, it is highly recommended to have a clean `git commit` state before running tasks!*
