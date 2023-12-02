import socket
import threading
from datetime import datetime, timedelta


# Определение класса сервера
class TaskServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tasks = {}
        self.task_id = 1
        self.lock = threading.Lock()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            print(f"Server started at {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                response = self.process_command(data.decode())
                conn.sendall(response.encode())

    def process_command(self, command):
        parts = command.strip().split(' ', 3)
        cmd = parts[0].upper()

        with self.lock:
            # Добавить задачу
            if cmd == 'ADD' and len(parts) == 4:
                summary, description, deadline_str = parts[1], parts[2], parts[3]
                try:
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                except ValueError:
                    return "Invalid date format. Please use YYYY-MM-DD."

                self.tasks[self.task_id] = {
                    "summary": summary,
                    "description": description,
                    "deadline": deadline
                }
                response = f"Task added with ID {self.task_id}"
                self.task_id += 1
            # Выводит список задач
            elif cmd == 'LIST':
                if not self.tasks:
                    response = "No tasks available"
                else:
                    response = "\n".join(
                        [f"{id}: {task['summary']} - {task['description']} - Due: {task['deadline'].date()}"
                         for id, task in self.tasks.items()])
            # Команда позволяет удалить таск по ид или по краткому описанию
            elif cmd == 'REMOVE' and len(parts) == 2:
                identifier = parts[1]
                task_found = False

                if identifier.isdigit():
                    task_id = int(identifier)
                    if task_id in self.tasks:
                        del self.tasks[task_id]
                        response = f"Task {task_id} removed"
                        task_found = True
                else:
                    for task_id, task in list(self.tasks.items()):
                        if task['summary'] == identifier:
                            del self.tasks[task_id]
                            response = f"Task '{identifier}' removed"
                            task_found = True
                            break

                if not task_found:
                    response = f"Task '{identifier}' not found"
            # Команда позволяет добавить более развернутое описание таску
            elif cmd == 'INSERT' and len(parts) == 3:
                identifier = parts[1]
                description = parts[2]
                task_updated = False

                if identifier.isdigit():
                    task_id = int(identifier)
                    if task_id in self.tasks:
                        self.tasks[task_id]["description"] = description
                        response = f"Description added to task {task_id}"
                        task_updated = True
                else:
                    for task_id, task in self.tasks.items():
                        if task['summary'] == identifier:
                            self.tasks[task_id]["description"] = description
                            response = f"Description added to task '{identifier}'"
                            task_updated = True
                            break

                if not task_updated:
                    response = f"Task '{identifier}' not found"
            # Команда показывает количество задач с дедлайном завтра
            elif cmd == 'DUE':
                current_date = datetime.now()
                due_tasks = [f"{id}: {task['summary']} - Due: {task['deadline'].date()}"
                             for id, task in self.tasks.items()
                             if task['deadline'] <= current_date + timedelta(days=1)]
                response = "\n".join(due_tasks) if due_tasks else "No tasks are due."
            # Ну тут понятно
            elif cmd == 'HELP':
                response = (
                    "Available commands:\n"
                    "ADD <summary> <description> <deadline> - Add a new task with a deadline (format YYYY-MM-DD).\n"
                    "LIST - List all tasks.\n"
                    "REMOVE <task_id> or <summary> - Remove a task by its ID or summary.\n"
                    "INSERT <task_id> or <summary> <description> - Update the description of a task.\n"
                    "DUE - List tasks with deadlines due today or tomorrow.\n"
                    "HELP - Show this help message."
                )
            else:
                response = "Invalid command"

            return response


# Запуск сервера
server = TaskServer('localhost', 65432)
server_thread = threading.Thread(target=server.start)
server_thread.start()
