from pydantic import BaseModel
from typing import Optional, Literal

class AgentAction(BaseModel):
    action: Literal[
        "search_code",
        "read_file",
        "propose_patch",
        "run_test",
        "final"
    ]
    reason: str
    query: Optional[str] = None
    path: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    find: Optional[str] = None
    replace: Optional[str] = None
    command: Optional[str] = None
    final_message: Optional[str] = None