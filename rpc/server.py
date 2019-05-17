
import socket
from server_framework import rpc_server_basic

if __name__ == '__main__':
    # create socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(1)

    # enter IO loop
    rpc_server_basic.loop(sock)
