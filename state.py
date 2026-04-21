from typing import List, Dict, Any, Optional

class AgentState:
    def __init__(self, task: str):
        self.task = task
        self.summary = f"Task: {task}"
        self.steps = 0
        self.max_steps = 20
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str, tool_calls: List[Dict[str, Any]] = None):
        msg = {"role": role, "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.messages.append(msg)

    def add_tool_response(self, content: str, tool_call_id: str = None, name: str = None):
        tool_msg = {"role": "tool", "content": content}
        if tool_call_id:
            tool_msg["tool_call_id"] = tool_call_id
        if name:
            tool_msg["name"] = name
        self.messages.append(tool_msg)
