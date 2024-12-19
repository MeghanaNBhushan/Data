"""
QAC Result helper class
"""


class QacResult:
    """QAC Result helper class"""

    def __init__(self, path, line_number, msg_text, severity, msg_id):
        self._path = path
        self._line_number = line_number
        self._msg_text = msg_text
        self._severity = severity
        self._teams = None
        self._components = None
        self._msg_id = msg_id

    def __repr__(self):
        return """QAC Result\n
                path: {0}\n
                line_number: {1}\n
                msg_text: {2}\n
                severity: {3}\n
                teams: {4}\n
                msg_id: {5}\n
                components: {6}\n__\n
                """.format(self._path, self._line_number, self._msg_text, self._severity, self._teams, self._msg_id, self._components)

    @property
    def path(self):
        return self._path

    @property
    def line_number(self):
        return self._line_number

    @property
    def msg_text(self):
        return self._msg_text

    @property
    def severity(self):
        return self._severity

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, value):
        self._teams = value

    @property
    def msg_id(self):
        return self._msg_id

    @property
    def components(self):
        return self._components

    @components.setter
    def components(self, value):
        self._components = value
