import json
from ollama_client import OllamaClient
from state import AgentState
from tools import search_code, read_file, propose_patch, run_test, git_diff, OLLAMA_TOOLS

SYSTEM_PROMPT = """
너는 초경량 고성능 코딩 에이전트다.

규칙:
1. 불필요한 설명은 최소화하고 필요한 action(tool_calls)을 즉시 실행해라.
2. 반드시 제공된 도구(tools)를 사용해서 작업을 수행해라.
3. 작업이 완료되면 'final' 도구를 호출하여 사용자에게 보고해라.
4. 'final' 호출 전까지는 자율적으로 도구를 사용해 문제를 해결해라.
"""

class CodingAgent:
    def __init__(self, host: str, model: str):
        self.client = OllamaClient(host=host, model=model)
        self.state = AgentState("Interactive Session")
        self.client.warmup()
        self.state.add_message("system", SYSTEM_PROMPT)

    def process_command(self, user_input: str):
        """사용자의 입력을 받아 도구 실행 루프를 시작함"""
        self.state.add_message("user", user_input)
        
        step = 0
        max_steps = 15 # 한 명령당 최대 자율 실행 단계

        while step < max_steps:
            step += 1
            
            # Ollama 호출
            response_msg = self.client.chat(messages=self.state.messages, tools=OLLAMA_TOOLS)
            
            content = response_msg.get("content", "")
            tool_calls = response_msg.get("tool_calls", [])
            
            self.state.add_message("assistant", content, tool_calls)

            if content:
                print(f"\n[AI] {content}")

            if not tool_calls:
                # 도구 호출이 없고 말만 있다면, 사용자의 추가 입력을 기다림
                return

            for tool_call in tool_calls:
                call_id = tool_call.get("id")
                func = tool_call.get("function", {})
                name = func.get("name")
                args = func.get("arguments", {})
                
                print(f"  └ [Action] {name}({args})")

                observation = ""
                if name == "search_code":
                    observation = search_code(args.get("query", ""))
                elif name == "read_file":
                    observation = read_file(args.get("path", ""), args.get("start_line", 1), args.get("end_line", 200))
                elif name == "propose_patch":
                    observation = propose_patch(args.get("path", ""), args.get("find", ""), args.get("replace", ""))
                elif name == "run_test":
                    observation = run_test(args.get("command", ""))
                elif name == "final":
                    print(f"\n[✔] 완료: {args.get('message', '작업 완료')}")
                    return # 이번 명령 처리 종료
                else:
                    observation = f"Unknown tool: {name}"

                # 도구 결과 피드백
                self.state.add_tool_response(observation, tool_call_id=call_id, name=name)
                
                obs_preview = observation[:150].replace("\n", " ") + "..." if len(observation) > 150 else observation
                print(f"  └ [Result] {obs_preview}")

        print("\n[!] 최대 단계를 초과했습니다. 계속하려면 명령을 입력하세요.")
