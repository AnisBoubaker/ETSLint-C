from reporters import BaseReporter


class PrintReporter(BaseReporter):
    def __init__(self):
        BaseReporter.__init__(self)

    def generate_report(self):
        reports = self.reports
        for report in reports:
            print("{}:{}:{} {} [{}]".format(report.file_name, report.line, report.column,
                                            report.message, str(report.rule)))

