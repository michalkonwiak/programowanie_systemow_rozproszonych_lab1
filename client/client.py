import csv
import socket
import struct
import time


def save_to_txt(command, diff_time_ms):
    data = command.split(";")
    str = ''
    for element in data:
        str += element + ","

    with open("wyniki1.txt", "a") as f:
        writer = csv.writer(f)
        writer.writerow([str, diff_time_ms])


def send_request(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))

    command_encoded = command.encode("utf-8")

    start_time = time.time()
    client.send(struct.pack("I", len(command_encoded)))
    client.send(command_encoded)
    response = receive_data(client)
    end_time = time.time()

    print("Server response:", response)
    diff_time_ms = (end_time - start_time) * 1000
    print(f"🚀 {diff_time_ms}ms")
    print("Command executed:", command)

    save_to_txt(command, diff_time_ms)
    client.close()


def receive_data(client_socket):
    response_length = struct.unpack("I", client_socket.recv(4))[0]
    data = b""
    while len(data) < response_length:
        part = client_socket.recv(min(4096, response_length - len(data)))
        if not part:
            break
        data += part

    return data.decode("utf-8")


def menu():
    while True:
        print("\nMenu:")
        print("1. Add student")
        print("2. Update student")
        print("3. Delete student")
        print("4. Retrieve students")
        print("5. Generate student's indexes")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            index = input("Input student index: ")
            send_request(f"add;{index}")
        elif choice == "2":
            old_index = input("Input old student index: ")
            new_index = input("Input new student index: ")
            send_request(f"update;{old_index};{new_index}")
        elif choice == "3":
            index = input("Input student index: ")
            send_request(f"delete;{index}")
        elif choice == "4":
            send_request("retrieve;")
        elif choice == "5":
            amount = input("Enter the number of students to generate (default 1000): ")
            send_request(f"generate;{amount}" if amount else "generate;")
        elif choice == "6":
            break
        else:
            print("Incorrect choice")


if __name__ == "__main__":
    menu()
