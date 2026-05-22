# Autobuild Manager GUI

The Autobuild Manager GUI is a standalone desktop application built with Python and PyQt5. it provides a user-friendly interface for managing virtual nodes via the project's `Makefile`.

## Features

- **Authentication**: Secure login required to access the manager.
- **Node Creation**: Specify an FQDN and select a role to create a new virtual node.
- **Node Deletion**: Quickly delete existing nodes with a confirmation prompt.
- **Real-time Console**: View live output from `make` commands directly in the application.
- **Automatic Logging**: All command outputs are automatically saved to the `logs/` directory with timestamps.

## Prerequisites

- Python 3
- PyQt5 (`pip install PyQt5`)

## Usage

To start the GUI, run the following command from the project root:

```bash
make gui
```

### Authentication
On the first run, the application will create a `.auth.json` file in the project root with default credentials:
- **Username**: `admin`
- **Password**: `password`

You can change these credentials by editing the `.auth.json` file. This file is excluded from git for security.

### Creating a Node
1. Enter the Full Qualified Domain Name (FQDN) in the text field (e.g., `webserver.example.com`).
2. Select the desired role from the dropdown menu (e.g., `apache`, `docker`).
3. Click **Create Node**. The output will appear in the console area below.

### Deleting a Node
1. Enter the FQDN of the node you wish to delete.
2. Click **Delete Node**.
3. Confirm the deletion in the popup dialog.

## Logging

Every operation performed via the GUI is logged to a file in the `logs/` directory. Files are named using the format `autobuild_YYYYMMDD_HHMMSS.log`. These logs include the command executed, start/end times, and the full console output.
