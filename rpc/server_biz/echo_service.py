
class EchoService:

    def __init__(self):
        self.visit_cnt = 0

    def hello(self, msg, attr=None):
        self.visit_cnt += 1
        if attr:
            print attr

        return {
            'code': '200',
            'visit_cnt': self.visit_cnt,
            'msg': msg
        }