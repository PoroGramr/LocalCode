import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any

def search_code(query: str) -> str:
    if not query.strip():
        return "[INFO] empty query"

    rg_path = shutil.which("rg")

    if rg_path:
        cmd = [rg_path, "-n", "-S", query, "."]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
        return output[:12000]

    # fallback: pure python search
    matched = []
    root = Path(".")

    skip_dirs = {
        ".git", "node_modules", ".next", "dist", "build",
        "__pycache__", ".venv", "venv", ".idea"
    }

    skip_exts = {
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf",
        ".zip", ".tar", ".gz", ".pyc", ".class"
    }

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in skip_dirs for part in path.parts):
            continue

        if path.suffix.lower() in skip_exts:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

        lines = text.splitlines()
        for idx, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                matched.append(f"{path}:{idx}:{line}")
                if len(matched) >= 200:
                    return "\n".join(matched)[:12000]

    if not matched:
        return f"[INFO] no matches for query: {query}"

    return "\n".join(matched)[:12000]

def read_file(path: str, start_line: int = 1, end_line: int = 200) -> str:
    p = Path(path)
    if not p.exists():
        return f"[ERROR] file not found: {path}"

    lines = p.read_text(encoding="utf-8").splitlines()
    start_idx = max(0, start_line - 1)
    end_idx = min(len(lines), end_line)

    selected = lines[start_idx:end_idx]
    numbered = [
        f"{i + start_line}: {line}"
        for i, line in enumerate(selected)
    ]
    return "\n".join(numbered)

def propose_patch(path: str, find: str, replace: str) -> str:
    p = Path(path)
    if not p.exists():
        return f"[ERROR] file not found: {path}"
    text = p.read_text(encoding="utf-8")

    if find not in text:
        return "[ERROR] target text (find) not found in file"

    new_text = text.replace(find, replace, 1)
    p.write_text(new_text, encoding="utf-8")
    return "[OK] patch applied"

def run_test(command: str) -> str:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    out = (result.stdout or "") + "\n" + (result.stderr or "")
    return out[:12000]

def git_diff() -> str:
    result = subprocess.run(["git", "diff", "--", "."], capture_output=True, text=True)
    return result.stdout[:20000]

# Tool Definitions for Ollama
OLLAMA_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Search for code patterns in the project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query or regex pattern"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read content of a file with line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "start_line": {"type": "integer", "description": "Starting line number (1-indexed)"},
                    "end_line": {"type": "integer", "description": "Ending line number (inclusive)"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "propose_patch",
            "description": "Apply a patch to a file by finding exactly one occurrence of 'find' and replacing it with 'replace'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "find": {"type": "string", "description": "Exact text to find"},
                    "replace": {"type": "string", "description": "Text to replace it with"}
                },
                "required": ["path", "find", "replace"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_test",
            "description": "Run a shell command, typically for tests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "final",
            "description": "End the agent loop when the task is complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Final summary message"}
                },
                "required": ["message"]
            }
        }
    }
]
