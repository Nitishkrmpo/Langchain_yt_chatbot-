from agent.agent_controller import AgentController
def run_cli():
    agent = AgentController()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = agent.process_request(user_input)
        print("Agent:", response)