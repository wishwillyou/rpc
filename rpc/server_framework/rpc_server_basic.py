import json
import struct
from server_biz import server_handler


def loop(sock):
    print "start listening ... "
    while True:
        conn, addr = sock.accept()
        handle_conn(conn, addr)


def handle_conn(conn, addr):
    print addr, "connected"
    while True:
        # receive message length
        length_prefix = conn.recv(4)
        if not length_prefix:
            print addr, "disconnected"
            conn.close()
            break
        # receive message body
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)
        request = json.loads(body)

        method = request['method']
        params = request['params']
        args = params['args'] or []
        kwargs = params['kwargs'] or {}
        print method, params
        handler = server_handler.handlers[method]
        result = handler(*args, **kwargs)
        send_result(conn, result)


def send_result(conn, result):
    response = json.dumps(result)
    length_prefix = struct.pack("I", len(response))
    conn.sendall(length_prefix)
    conn.sendall(response)
