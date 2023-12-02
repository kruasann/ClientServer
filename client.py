import socket


# Определение класса клиента
class TaskClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_command(self, command):
        # Отправка команды на сервер и получение ответа
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(command.encode())
            response = s.recv(1024)
            return response.decode()


def run_client():
    client = TaskClient('localhost', 65432)

    while True:
        # Получение команды от пользователя
        command = input("Enter command (ADD, LIST, REMOVE, INSERT, DUE, HELP, QUIT to exit): ")

        # Обработка команды выхода
        if command.upper() == "QUIT":
            print("Exiting client...")
            break

        # Отправка команды и получение ответа от сервера
        response = client.send_command(command)
        print("Response from server:", response)


run_client()
