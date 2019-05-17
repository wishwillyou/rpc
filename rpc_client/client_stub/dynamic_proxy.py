from types import MethodType
import socket
import json
import struct


global_sock = None


def socket_connect():
    global global_sock
    if global_sock:
        return global_sock
    global_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global_sock.connect(("localhost", 8080))
    return global_sock


class InvocationHandler:
    def __init__(self, obj, func):
        self.obj = obj
        self.func = func

    def __call__(self, *args, **kwargs):
        # if you want to execute origin method, just execute
        # return self.func(*args, **kwargs)

        clz = self.obj.__class__.__name__
        mtd = self.func.__name__
        req = clz[0].lower() + clz[1:] + '.' + mtd
        request = json.dumps({
            'method': req,
            'params': {
                'args': args,
                'kwargs': kwargs
            }
        })

        sock = socket_connect()
        length_prefix = struct.pack("I", len(request))
        sock.sendall(length_prefix)
        sock.sendall(request)
        length_prefix = sock.recv(4)
        length, = struct.unpack("I", length_prefix)
        body = sock.recv(length)
        return json.loads(body)


class HandlerException(Exception):
    def __init__(self, cls):
        super(HandlerException, self).__init__(cls, 'is not a hanlder class')


class Proxy:
    def __init__(self, cls, hcls):
        self.cls = cls
        self.hcls = hcls
        self.handlers = dict()

    def __call__(self, *args, **kwargs):
        self.obj = self.cls(*args, **kwargs)
        return self

    def __getattr__(self, attr):
        isExist = hasattr(self.obj, attr)
        res = None
        if isExist:
            res = getattr(self.obj, attr)
            if isinstance(res, MethodType):
                if self.handlers.get(res) is None:
                    self.handlers[res] = self.hcls(self.obj, res)
                return self.handlers[res]
            else:
                return res
        return res


class ProxyFactory:
    def __init__(self, hcls):
        if issubclass(hcls, InvocationHandler) or hcls is InvocationHandler:
            self.hcls = hcls
        else:
            raise HandlerException(hcls)

    def __call__(self, cls):
        return Proxy(cls, self.hcls)

