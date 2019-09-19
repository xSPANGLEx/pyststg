from lib import audit


class Audit(audit.Auditor):

    @property
    def regex_word(self) -> str:
        return r'BEGIN PRIVATE KEY'
