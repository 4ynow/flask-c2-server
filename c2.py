import requests
import os

def list_agents():
    list_of_agents = requests.get("https://127.0.0.1:4000/list", verify=False)
    print(list_of_agents.json())

def get_result(agent_id):
    result = requests.get("https://127.0.0.1:4000/result/" + agent_id, verify=False)
    print(result.json())

def set_task(agent_id, command):
    result = requests.post(
        "https://127.0.0.1:4000/task/" + agent_id,
        json={"command": command},
        verify=False
    )
    print(result.json())

print("Welcome to the C2 CLI. Type 'quit' to exit.")

try:
    while True:
        i = input("c2> ").split()

        if not i:
            continue

        command = i[0]

        if command == "list":
            if len(i) != 1:
                print("Please use 'list' only.")
            else:
                list_agents()

        elif command == "results":
            if len(i) != 2:
                print("Please use ID only.")
            else:
                get_result(i[1])

        elif command == "task":
            if len(i) < 3:
                print("Please enter a valid task.")
            else:
                full_command = " ".join(i[2:])
                set_task(i[1], full_command)

        elif command == "help":
            if len(i) != 1:
                print("Please use 'help' only.")
            else:
                print("Available commands:")
                print("  list                  Show all registered agents")
                print("  results <agent_id>    Show results for a specific agent")
                print("  task <agent_id> <command>  Send a command to an agent")
                print("  kill                  Wipe all agents, results, and tasks")
                print("  clear                 Clear the screen")
                print("  quit                  Exit the CLI")

        elif command == "quit" or command == "exit":
            if len(i) != 1:
                print("Please use 'quit' only.")
            else:
                break

        elif command == "kill":
            if len(i) != 1:
                print("Please use 'kill' only.")
            else:
                response = requests.post("https://127.0.0.1:4000/kill", verify=False)
                print(response.json())

        elif command == "clear":
            if len(i) != 1:
                print("Please enter the command only.")
            else:
                os.system("clear")

        else:
            print("Unknown command!")

except KeyboardInterrupt:
    print("\nExiting...")