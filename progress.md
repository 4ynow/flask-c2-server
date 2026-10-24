# Development Progress

## Project Status: In Progress

### Completed
* Built initial Flask backend (server.py) with TLS and XOR encryption.
* Built Python agent (agent.py) with task execution and persistence.
* Built CLI controller (c2.py).
* Enabled CORS on the Flask server for frontend communication.
* Added threading to Flask to handle simultaneous agent check-ins.

### In Progress
* Building the Web Dashboard (HTML/CSS/JS).

### To-Do (Backend)
* Switch storage from JSON to SQLite to prevent data corruption.
* Implement Long Polling to reduce agent check-in delays.
* Add API authentication (Bearer tokens) to secure the C2 server.

### To-Do (Frontend Dashboard)
* Create the HTML/CSS skeleton (Sidebar for agents, terminal window, input bar).
* Connect JavaScript fetch() to the /list endpoint to display active agents.
* Implement POST requests to send commands to active agents.
* Create a setInterval loop to fetch and display live command results.

### Known Issues
* Self-signed SSL certificate blocks browser fetch() requests until manually accepted.
