from server_biz.echo_service import EchoService

echoService = EchoService()

handlers = {
    'echoService.hello': echoService.hello
}