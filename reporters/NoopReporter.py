from reporters import BaseReporter


class NoopReporter(BaseReporter):
    def __init__(self):
        BaseReporter.__init__(self)

    def generate_report(self):
        pass
