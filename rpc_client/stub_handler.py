import time

from client_stub.echo_service import EchoService

if __name__ == '__main__':
    echo_service = EchoService()
    print echo_service.hello('world', attr={'a': 1})

