import socket
import select

# Constants
MAX_CLIENTS = 1000
SERVER_PORT = 7711


# Client class
class Client:
    def __init__(self, sock, addr):
        self.socket = sock
        self.addr = addr
        self.nick = f"user:{addr[1]}"


# Chat class
class Chat:
    def __init__(self):
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", SERVER_PORT))
        self.server_socket.listen(511)
        self.client_sockets = [self.server_socket]

    def add_client(self, client_socket, addr):
        client = Client(client_socket, addr)
        self.clients[client_socket] = client
        self.client_sockets.append(client_socket)

        welcome_msg = "Welcome to Simple Chat! Use /nick <nick> to set your nick.\n"
        client_socket.send(welcome_msg.encode())
        print(f"Connected client {addr[1]}")

    def remove_client(self, client_socket):
        print(
            f"Disconnected client {self.clients[client_socket].addr[1]}, nick={self.clients[client_socket].nick}"
        )
        del self.clients[client_socket]
        self.client_sockets.remove(client_socket)

    def run(self):
        while True:
            rlist, _, _ = select.select(self.client_sockets, [], [], 1)

            for ready_socket in rlist:
                if ready_socket == self.server_socket:
                    client_socket, addr = self.server_socket.accept()
                    self.add_client(client_socket, addr)
                else:
                    try:
                        data = ready_socket.recv(256)
                        if not data:
                            self.remove_client(ready_socket)
                        else:
                            client = self.clients[ready_socket]

                            if data[0] == b"/":
                                args = data.decode()[1:].split(" ")
                                cmd = args[0]
                                if cmd == "nick" and len(args) > 1:
                                    client.nick = args[1]
                                else:
                                    errmsg = "Unsupported command\n"
                                    ready_socket.send(errmsg.encode())

                            else:
                                msg = f"{client.nick}> {data.decode()}".encode()
                                print(msg.decode(), end="")

                                for sock in self.clients:
                                    if sock != ready_socket:
                                        sock.send(msg)

                    except Exception:
                        self.remove_client(ready_socket)


if __name__ == "__main__":
    chat = Chat()
    chat.run()
