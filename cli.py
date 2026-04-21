import argparse
import sys
from agent import CodingAgent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True, help="Ollama server host (e.g., http://192.168.1.100:11434)")
    parser.add_argument("--model", type=str, required=True, help="Ollama model name (e.g., llama3.1:8b)")
    args = parser.parse_args()

    # 에이전트 초기화 (맥 스튜디오와 연결)
    agent = CodingAgent(host=args.host, model=args.model)

    print("\n🚀 Ollama Native Coding Agent가 준비되었습니다.")
    print("종료하려면 'exit' 또는 'quit'을 입력하세요.\n")

    while True:
        try:
            # 사용자 입력 대기
            user_input = input("👤 > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 종료합니다.")
                break

            # 에이전트에게 명령 전달 및 자율 실행 시작
            agent.process_command(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 인터럽트로 종료합니다.")
            break
        except Exception as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    main()
