<div style="border: 1px solid #dadada; padding: 20px; border-radius: 6px; background-color: #f6f8fa; color: #24292f;">

# Flask C2 Server & Dashboard

A custom **Command & Control (C2) framework** built for educational purposes and lab environments. It features an interactive operator CLI, task queuing, result collection, TLS support, basic XOR encryption for payloads, a web dashboard, and a kill switch.

### Disclaimer
This project is for **educational purposes only**. Use it only on systems you own or have permission to test.

### Features
* **Web Dashboard:** A graphical frontend to control agents and view live output.
* **Interactive CLI:** Operator console with commands: `list`, `task`, `results`, `kill`, `clear`, `help`, `quit`.
* **Agent Registration:** Tracks hostname, IP, and timestamps.
* **Task Queue:** Operator sets a command, the agent picks it up.
* **Result Collection:** Agent sends output back, server stores it.
* **TLS Encryption:** For transport security.
* **XOR Encryption:** For task and result payloads (Base64 encoded).
* **Kill Switch:** Clears all data and deletes storage.
* **Persistence:** Saves agent and server data using JSON.

### Project Structure
```text
C2-Project/
│
├── backend/
│   ├── server.py (Flask server, handles all HTTP routes)
│   ├── agent.py (The payload that runs on the target machine)
│   ├── c2.py (Interactive operator console)
│   └── requirements.txt (Python dependencies)
│
├── c2-dashboard/ (Web-based frontend interface)
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── README.md (This file)
```

### Installation
Clone the repo and install dependencies:
```bash
git clone <your-repo-url>
cd <repo-name>/backend
sudo apt install python3-flask python3-flask-cors python3-requests
```

### TLS Certificates
Generate a self-signed certificate and key for the server to use TLS:
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
*The server will look for `cert.pem` and `key.pem` in the same directory. Do not commit these files to the repo.*

### Running the Server
Start the Flask server:
```bash
python server.py
```
*(The server runs on `https://127.0.0.1:4000` by default).*

### Running the Operator CLI
In a separate terminal:
```bash
python c2.py
```
*You'll see a `c2>` prompt. Type `help` for a list of commands.*

### Commands

| Command | Description |
| :--- | :--- |
| **list** | Show all registered agents |
| **task &lt;agent_id&gt; &lt;command&gt;** | Queue a command for a specific agent |
| **results &lt;agent_id&gt;** | Show results for a specific agent |
| **kill** | Clear all agents, results, tasks, and delete storage |
| **clear** | Clear the terminal screen |
| **help** | Show available commands |
| **quit** | Exit the CLI |

### Encryption
The agent and server use **XOR encryption with base64 encoding**. The XOR key is hardcoded as `0x42`. This hides the command and output from anyone watching the traffic. It's simple, but it's not strong encryption. If you need real security, replace it with **AES**.

</div>
