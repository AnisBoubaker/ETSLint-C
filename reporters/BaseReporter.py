
class Report(object):
    def __init__(self, rule, coord, message):
        self.__rule = rule
        self.__file_name = coord.file
        self.__column = coord.column
        self.__line = coord.line
        self.__message = message

    @property
    def rule(self):
        return self.__rule

    @property
    def file_name(self):
        return self.__file_name

    @property
    def column(self):
        return self.__column

    @property
    def line(self):
        return self.__line

    @property
    def message(self):
        return self.__message


class BaseReporter(object):

    def __init__(self):
        self.__reports = []

    @property
    def reports(self):
        return self.__reports

    def do_report(self, rule, coord, message):
        self.__reports += [Report(rule, coord, message)]

    def generate_report(self):
        print("Error: Base reporter cannot generate a report.")
