import socket
import threading
from attr import define


@define
class Server:
    """
    Make connection with server according requests of clients.
    Args:
        port: Service that we wanna connect.
        host: IP of machine that we can connect to a network.
        server_socket: inter-process communication (IPC)
    """

    port: str
    host: str = "localhost"
    server_socket: None | socket.socket = None

    @classmethod
    def from_dict(cls, config_dict):
        return cls(**config_dict)

    def _make_conn(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(("Server listening on port", self.port))

    def _client_handler(self, client_socket):
        data = client_socket.recv(1024).decode()
        print(f"System's response: {data}")

        if not data:
            client_socket.close()
            return

        parts = data.split(" ", 1)
        command = parts[0]
        message = parts[1] if len(parts) > 1 else ""

        if command == "echo":
            client_socket.send(("Echo: " + message).encode())
            self._client_handler(client_socket)
        elif command == "quit":
            return
            if client_socket:
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
        else:
            client_socket.send("Unknown command".encode())

    def start(self):
        self._make_conn()

        while True:
            print("Server is running and waiting for connections...")
            client_socket, addr = self.server_socket.accept()
            print("Accepted connection from", addr)

            client_thread = threading.Thread(
                target=self._client_handler, args=(client_socket,)
            )
            client_thread.start()

    def close(self):
        self.server_socket.close()


class EchoServer:
    """
    Global variable:
        self_server: Instance of Server class. This variable is initialized with dict whose keys are host(opitional) and port.
    Case the user don't set the host, the default to this parameter is localhost
    """

    @property
    def get_start(self):
        return self._server

    @get_start.setter
    def get_start(self, server_dict: dict) -> None:
        self._server = server_dict
        s = Server.from_dict(self._server)
        s.start()
        s.close()
        return


if __name__ == "__main__":
    server_dict = {"host": "localhost", "port": 8080}
    es = EchoServer()
    es.get_start = server_dict
