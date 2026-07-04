# Autobuild Web UI

A web interface for automating node deployments via an underlying Makefile.

## Features

- **Web Interface**: Modern, responsive web UI for creating and deleting nodes.
- **Makefile Integration**: Directly executes `make` commands to manage infrastructure.

## Project Structure

```text
/
├── server.js          # Node.js Express server (Web Backend)
├── package.json       # Node.js dependencies and scripts
├── public/            # Web Frontend assets
│   ├── index.html     # Web UI structure
│   ├── script.js      # Web UI logic
│   └── style.css      # Web UI styling
└── README.md          # Project documentation
```

## Prerequisites

- **Node.js**: Required for the Web Interface.
- **Make**: The project expects a `Makefile` in the parent directory (or at `/home/sandholm/prog/autobuild/Makefile`).

## Getting Started

### Web Interface

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start the Server**:
   ```bash
   npm start
   ```

3. **Access the UI**:
   Open [http://localhost:3000](http://localhost:3000) in your browser.

## How It Works

### Web Interface
The web interface communicates with `server.js` via API endpoints:
- `POST /api/node`: Executes `make node NAME={fqdn} ROLE={role}`.
- `POST /api/delete`: Executes `make Delete NAME={fqdn}`.
