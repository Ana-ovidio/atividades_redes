"""
Make connection with server into 8080 port service. 
The uniques requeirements is the user input a text (echo/quit) guiding the code to execute it longs
Args:
    localhost = Connect to our local machine IP
    port = Service that we wanna connect
"""
import socket


def main():
    host = "localhost"
    port = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Put a message (echo/quit): ")
        if message == "quit":
            client_socket.send(message.encode())
            client_socket.close()
            break
        elif message == "echo":
            message = input("Send a message to echo: ")
            client_socket.send(f"echo {message}".encode())
        else:
            print("Unkown command. Use 'echo' or 'quit'.")

    client_socket.close()


if __name__ == "__main__":
    main()
