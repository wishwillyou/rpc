import json
import time
import struct
import socket


def rpc(sock, target, args=None, kwargs=None):
    request = json.dumps({"method": target, "params": {'args': args, 'kwargs': kwargs}})
    length_prefix = struct.pack("I", len(request))
    sock.sendall(length_prefix)
    sock.sendall(request)
    length_prefix = sock.recv(4)
    length, = struct.unpack("I", length_prefix)
    body = sock.recv(length)
    return json.loads(body)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    for i in range(10):
        result = rpc(s, "echoService.hello", ["world %d" % i])
        print result
        time.sleep(1)
    s.close()