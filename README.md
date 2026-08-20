# Advanced Flask-Based Command & Control (C2) Framework

A robust, lightweight Command and Control (C2) architecture featuring a Flask-driven HTTP operational server and an interactive CLI management interface. This framework supports authenticated agent lifecycle management, encrypted tasking workflows, and secure transport layers.

> **Disclaimer & Safety Notice**
> This repository is developed strictly for academic research, educational purposes, and authorized security assessments. The implant/agent source code (`agent.py`) has been intentionally omitted from this public repository to prevent misuse and strictly comply with security and hosting platform safety policies. Users are entirely responsible for their own testing environments and target authorizations.

---

## Technical Overview & Features

*   **Asynchronous Interactive Operator Console:** A full-featured Command Line Interface (CLI) (`c2.py`) equipped with dedicated context commands for administrative overhead and agent tasks.
*   **Flask HTTP Restful Backend:** A scalable HTTP server (`server.py`) managing dynamic endpoints for client registration, secure heartbeats, and transactional queues.
*   **Encrypted Payload & Tasking Workflows:** Native implementation of state-based tracking, task staging, and dynamic result aggregation, with standard **XOR obfuscation/encryption** routines for secure operational flows.
*   **Transport Layer Security (TLS):** End-to-end payload transit encryption via HTTPS integration.
*   **Defensive Safeguards & Emergency Kill-Switch:** Built-in mechanism to completely purge agent history, active staging queues, and database records instantly from memory upon operator signal.

---

## Directory Infrastructure

```text
├── server.py        # Central Flask-based HTTP server managing tracking, tasks, and data ingestion.
├── c2.py            # Operational interactive command-line suite for target administration.
├── requirements.txt # Project dependency manifests (Flask, requests).
└── README.md        # Technical architecture documentation.
```

---

## Installation & Deployment

### 1. Environment Configuration
Clone the repository and install the framework dependencies within a clean virtual environment:

```bash
git clone <your-repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

### 2. Mandatory SSL/TLS Configuration
To preserve transport security over HTTP, the server expects valid TLS configurations. Cryptographic certificates (`cert.pem`) and private keys (`key.pem`) have been omitted from the repository layout. You must explicitly generate a local self-signed key pair using OpenSSL prior to executing the runtime:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

Ensure `cert.pem` and `key.pem` reside within the root workspace directory before starting the runtime environment.

### 3. Launching the Management Server
Initialize the listener service by executing the main backend thread:

```bash
python server.py
```

### 4. Running the Operator Console
In a separate terminal workspace, initiate the interactive orchestration interface to manage connected endpoints:

```bash
python c2.py
```

---

## Operator Console Interface Reference

The `c2.py` operational prompt supports the following operational commands:

| Command | Action / Usage Description |
| :--- | :--- |
| `list` | Enumerate all persistently registered agents and their current check-in metrics. |
| `task` | Staging a new XOR-encrypted operational task sequence for a specified agent ID. |
| `results` | Query, fetch, and display ingested execution results returned by a target. |
| `kill` | Broadcast a destructive kill-switch signal to clear active memory and operational state. |
| `clear` | Clear the active terminal workspace screen context. |
| `help` | Display structural parameter syntax and contextual instructions. |
| `quit` | Gracefully detach and exit the local operator control terminal. |
