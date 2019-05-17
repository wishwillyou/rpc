import asyncore
import json
import socket
import struct
from cStringIO import StringIO

from server_biz import server_handler


class RPCHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        self.addr = addr
        self.rbuf = StringIO()

    def handle_read(self):
        while True:
            content = self.recv(1024)
            if content:
                self.rbuf.write(content)
            if len(content) < 1024:
                break
        self.handle_rpc()

    def handle_rpc(self):
        while True:
            self.rbuf.seek(0)
            length_prefix = self.rbuf.read(4)
            if len(length_prefix) < 4:
                break
            length, = struct.unpack('I', length_prefix)
            body = self.rbuf.read(length)
            if len(body) < length:
                break
            request = json.loads(body)

            method = request['method']
            params = request['params']
            args = params['args'] or []
            kwargs = params['kwargs'] or {}
            print method, params
            handler = server_handler.handlers[method]
            result = handler(*args, **kwargs)
            self.send_result(result)
            left = self.rbuf.getvalue()[length + 4:]
            self.rbuf = StringIO()
            self.rbuf.write(left)

    def send_result(self, result):
        response = json.dumps(result)
        length_prefix = struct.pack("I", len(response))
        self.send(length_prefix)
        self.send(response)


class RPCServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            RPCHandler(sock, addr)

