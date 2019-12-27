from clinter.reporters import BaseReporter


class PrintReporter(BaseReporter):
    def __init__(self):
        BaseReporter.__init__(self)

    def generate_report(self):
        reports = self.reports
        current_file_name = None
        for report in reports:
            if current_file_name is None or report.file_name != current_file_name:
                current_file_name = report.file_name
                print("**** Reports for file: " + current_file_name)
            print("{}:{}:{} {} [{}]".format(report.file_name, report.line, report.column,
                                            report.message, str(report.rule)))
