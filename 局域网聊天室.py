import socket
import select

# Constants
MAX_CLIENTS = 1000
SERVER_PORT = 7711


# Client class
class Client:
    # 初始化函数，创建一个socket，用于客户端，创建一个字符串，用于存储客户端的昵称
    def __init__(self, sock, addr):
        self.socket = sock
        self.addr = addr
        self.nick = f"user:{addr[1]}"


# Chat class
class Chat:
    # 初始化函数，创建一个字典，用于存储客户端，创建一个socket，用于服务器，绑定服务器地址和端口，创建一个列表，用于存储客户端的socket
    def __init__(self):
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", SERVER_PORT))
        self.server_socket.listen(511)
        self.client_sockets = [self.server_socket]

    # 添加客户端函数，将客户端的socket和地址加入到字典和列表中
    def add_client(self, client_socket, addr):
        client = Client(client_socket, addr)
        self.clients[client_socket] = client
        self.client_sockets.append(client_socket)

        welcome_msg = "Welcome to Simple Chat! Use /nick <nick> to set your nick.\n"
        client_socket.send(welcome_msg.encode())
        print(f"Connected client {addr[1]}")

    # 删除客户端函数，将客户端的socket和地址从字典和列表中删除
    def remove_client(self, client_socket):
        print(
            f"Disconnected client {self.clients[client_socket].addr[1]}, nick={self.clients[client_socket].nick}"
        )
        del self.clients[client_socket]
        self.client_sockets.remove(client_socket)

    def run(self):
        while True:
            # 使用select函数，监听客户端socket，如果有客户端socket有数据发送过来，就将其加入到rlist列表中
            rlist, _, _ = select.select(self.client_sockets, [], [], 1)

            # 遍历rlist列表，处理客户端socket发送过来的数据
            for ready_socket in rlist:
                # 如果是服务器socket，说明有新的客户端连接，调用add_client函数，将其加入到字典和列表中
                if ready_socket == self.server_socket:
                    client_socket, addr = self.server_socket.accept()
                    self.add_client(client_socket, addr)
                # 如果不是服务器socket，说明是已经连接的客户端发送数据过来，调用recv函数接收数据
                else:
                    try:
                        # 接收数据，最大长度为256字节
                        data = ready_socket.recv(256)
                        # 如果接收到的数据为空，说明客户端已经断开连接，调用remove_client函数，将其从字典和列表中删除
                        if not data:
                            self.remove_client(ready_socket)
                        # 如果接收到的数据不为空，说明客户端发送了数据过来，将其发送给其他客户端
                        else:
                            # 获取发送数据的客户端的昵称
                            client = self.clients[ready_socket]

                            # 如果发送的数据以"/"开头，说明是命令，将其解析
                            if data[0] == b"/":
                                args = data.decode()[1:].split(" ")
                                cmd = args[0]
                                if cmd == "nick" and len(args) > 1:
                                    client.nick = args[1]
                                else:
                                    errmsg = "Unsupported command\n"
                                    ready_socket.send(errmsg.encode())

                            # 如果发送的数据不是以"/"开头，说明是聊天信息，将其发送给其他客户端
                            else:
                                msg = f"{client.nick}> {data.decode()}".encode()
                                print(msg.decode(), end="")

                                # 遍历客户端的socket，将消息发送给其他客户端
                                for sock in self.clients:
                                    if sock != ready_socket:
                                        sock.send(msg)

                    except Exception:
                        self.remove_client(ready_socket)


if __name__ == "__main__":
    chat = Chat()
    chat.run()
