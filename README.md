## Available Commands

### Client Commands

- `ADD "summary" "description" "deadline"`: Add a new task with a deadline. The deadline should be in the format YYYY-MM-DD.
- `LIST`: List all tasks. Shows the summary, description, and deadline of each task.
- `REMOVE "task_id" or "summary"`: Remove a task by its ID or summary.
- `INSERT "task_id" or "summary" "description"`: Update the description of an existing task.
- `DUE`: List tasks with deadlines that are due today or tomorrow.
- `HELP`: Show the available commands and their usage.
- `QUIT`: Exit the client application.

### Server

The server runs continuously, listening for client requests and responding to them according to the commands received.

## Setup and Running

### Server

1. Start the server by running the `server.py` script.
2. The server will start listening for incoming client connections.

### Client

1. Start the client by running the `client.py` script.
2. Use the above commands to interact with the server.
