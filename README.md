# Flask C2 Server

A simple command-and-control server written in Flask. It has an interactive operator CLI, task queuing, result collection, TLS support, basic XOR encryption for payloads, and a kill switch. The agent component is not included for legal and safety reasons.

## Features

- Interactive operator CLI with commands: `list`, `task`, `results`, `kill`, `clear`, `help`, `quit`
- Agent registration with hostname, IP, and timestamps
- Task queue: operator sets a command, agent picks it up
- Result collection: agent sends output back, server stores it
- TLS encryption for transport
- XOR encryption for task and result payloads
- Kill switch to clear all data and delete storage
- Persistent agent and server data using JSON

## Project Structure

```
server.py        # Flask server, handles all HTTP routes
c2.py            # Interactive operator console
requirements.txt # Python dependencies
README.md        # This file
```

The agent code is intentionally not included.

## Installation

Clone the repo and install dependencies:

```
git clone <your-repo-url>
cd <repo-name>
pip install -r requirements.txt
```

## TLS Certificates

You need to generate a self-signed certificate and key for the server to use TLS.

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

The server will look for `cert.pem` and `key.pem` in the same directory. Do not commit these files to the repo.

## Running the Server

Start the Flask server:

```
python server.py
```

The server runs on `https://127.0.0.1:4000`.

## Running the Operator CLI

In a separate terminal:

```
python c2.py
```

You'll see a `c2>` prompt. Type `help` for a list of commands.

## Commands

| Command | Description |
|---------|-------------|
| `list` | Show all registered agents |
| `task <agent_id> <command>` | Queue a command for a specific agent |
| `results <agent_id>` | Show results for a specific agent |
| `kill` | Clear all agents, results, tasks, and delete storage |
| `clear` | Clear the terminal screen |
| `help` | Show available commands |
| `quit` | Exit the CLI |

## Encryption

The agent and server use XOR encryption with base64 encoding. The XOR key is hardcoded as `0x42`. This hides the command and output from anyone watching the traffic. It's simple, but it's not strong encryption. If you need real security, replace it with AES.

## Kill Switch

When the operator sends `kill` through the CLI, the server clears `agents`, `results`, and `tasks`, and deletes `c2_data.json`. The agent also has a kill command that deletes its ID file and stops running.

## Disclaimer

This project is for educational purposes only. Use it only on systems you own or have permission to test. The agent component is omitted to prevent misuse.
| `help` | Display structural parameter syntax and contextual instructions. |
| `quit` | Gracefully detach and exit the local operator control terminal. |
