import socket

def send_request(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))

    client.send(command.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print("Server response:", response)

    client.close()

def menu():
    while True:
        print("\nMenu:")
        print("1. Add team")
        print("2. Update team")
        print("3. Delete team")
        print("4. Get info about teams")
        print("5. Generate random teams")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            name = input("Input team name: ")
            send_request(f"add;{name}")
        elif choice == "2":
            old_name = input("Input old team name: ")
            new_name = input("Input new team name: ")
            send_request(f"update;{old_name};{new_name}")
        elif choice == "3":
            name = input("Input team name: ")
            send_request(f"delete;{name}")
        elif choice == "4":
            send_request("retrieve;")
        elif choice == "5":
            amount = input("Enter the number of teams to generate (default 1000): ")
            send_request(f"generate;{amount}" if amount else "generate;")
        elif choice == "6":
            break
        else:
            print("Incorrect choice")

if __name__ == "__main__":
    menu()
