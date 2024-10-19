import re
import socket
import struct
import threading


from dto import DeansOffice, Student

deans_office = DeansOffice()


def validate_student_name(name):
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
            if command == "add" and validate_student_name(args[0]):
                if deans_office.add_student(Student(args[0])):
                    result = "Student added"
                else:
                    result = "Student name already exists"

            elif command == "update" and validate_student_name(args[1]):
                if deans_office.update_student(args[0], args[1]):
                    result = "Student updated"
                else:
                    result = "Student not found"

            elif command == "delete":
                deans_office.delete_student(args[0])
                result = "Student deleted"

            elif command == "retrieve":
                result = ', '.join(deans_office.get_students())

            elif command == "generate":
                amount = int(args[0]) if args and args[0].isdigit() else 1000
                deans_office.generate_random_students(amount)
                result = f"{amount} random students generated"

            else:
                result = "Invalid command or input"

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
    deans_office = DeansOffice()
    run_server()
