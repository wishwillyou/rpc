import asyncore

from server_framework.rpc_server_nio import RPCServer

if __name__ == '__main__':
    RPCServer("localhost", 8080)
    asyncore.loop()
