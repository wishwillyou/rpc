from client_stub.dynamic_proxy import ProxyFactory, InvocationHandler


@ProxyFactory(InvocationHandler)
class EchoService:
    def __init__(self):
        pass

    def hello(self, msg, attr=None):
        raise Exception('stub class')
