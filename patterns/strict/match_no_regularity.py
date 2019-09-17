from lib import audit


class Audit(audit.Auditor):

    @property
    def regex_word(self) -> str:
        return r'(\s|")([0-9]|[a-z]|[A-Z]){32,128}( |"|$)'
