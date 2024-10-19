import re
import socket
import struct
import threading
import csv
import time

from dto import League, Team

league = League()

def validate_team_name(name):
    if re.match("^[A-Za-z0-9_]+$", name) and len(name) <= 30:
        return True
    return False


def receive_data(client_socket):
    data = b""

    while len(data) < 4:
        packet = client_socket.recv(4 - len(data))
        if not packet:
            return None
        data += packet

    response_length = struct.unpack("I", data)[0]

    data = b""
    while len(data) < response_length:
        part = client_socket.recv(response_length - len(data))
        if not part:
            return None
        data += part

    return data.decode('utf-8')


def client_service(client_socket, address):
    print(f"Connected to {address}")

    try:
        while True:
            data = receive_data(client_socket)
            if not data:
                break

            command, *args = data.split(';')
            result = ""
            start_time = time.time()

            if command == "add" and validate_team_name(args[0]):
                if league.add_team(Team(args[0])):
                    result = "Team added"
                else:
                    result = "Team name already exists"

            elif command == "update" and validate_team_name(args[1]):
                if league.update_team(args[0], args[1]):
                    result = "Team updated"
                else:
                    result = "Team not found"

            elif command == "delete":
                league.delete_team(args[0])
                result = "Team deleted"

            elif command == "retrieve":
                result = ', '.join(league.get_teams())

            elif command == "generate":
                amount = int(args[0]) if args and args[0].isdigit() else 1000
                league.generate_random_teams(amount)
                result = f"{amount} random teams generated"

            else:
                result = "Invalid command or input"

            end_time = time.time()
            diff_time_ms = (end_time - start_time) * 1000

            with open('wyniki1.txt', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([args[0] if args else 'n/a', command, diff_time_ms])

            result_encoded = result.encode('utf-8')
            client_socket.send(struct.pack("I", len(result_encoded)))
            client_socket.send(result_encoded)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1)
    print("Server is waiting for a connection")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=client_service, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    league = League()
    run_server()
