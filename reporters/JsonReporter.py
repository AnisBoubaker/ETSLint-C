from reporters import BaseReporter
import json


class JsonReporter(BaseReporter):
    def __init__(self, file_output=None):
        BaseReporter.__init__(self)
        self.__file_output = file_output

    def generate_report(self):
        result = {}
        reports = self.reports
        for report in reports:
            if report.file_name not in result:
                result[report.file_name] = []

            result[report.file_name] += [{'file': report.file_name,
                                          'line': report.line,
                                          'column': report.column,
                                          'rule': str(report.rule),
                                          'message': report.message}]

        if self.__file_output is not None:
            with open(self.__file_output, "w", encoding="utf-8") as file:
                json.dump(result, file, indent=True)

        return json.dumps(result, indent=True)
