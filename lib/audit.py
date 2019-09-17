import glob
import importlib

from lib import git


class Auditor(object):

    def __init__(self, repository) -> None:
        self.repository = repository

    def extend_filter(self) -> str:
        return ""

    @property
    def regex_word(self) -> str:
        raise NotImplementedError()

    def audit(self) -> str:
        return self.repository.grep(self.regex_word)


class AuditMode(object):
    @property
    def permissive(self):
        return "PERMISSIVE"

    @property
    def strict(self):
        return "STRICT"


class UnSupportedModeError(Exception):
    pass


class Audit(object):

    def __init__(self, repository, mode=AuditMode().strict):
        self.repository = git.Git(repository)
        self.audit_mode = mode

    def execute(self):
        if self.audit_mode == AuditMode().strict:
            modules = [
                    name.split(".py")[0].replace("/", ".")
                    for name in glob.glob("patterns/strict/*")
                    if name.endswith(".py")
                    ]
        elif self.audit_mode == AuditMode().permissive:
            modules = [
                    name.split(".py")[0].replace("/", ".")
                    for name in glob.glob("patterns/permissive/*")
                    if name.endswith(".py")
                    ]
        else:
            raise UnSupportedModeError(f"Unsupported mode {self.audit_mode}")
        auditors = [
                importlib.import_module(module)
                for module in modules
                ]
        results = []
        for auditor in auditors:
            result = auditor.Audit(self.repository).audit()
            results.append(result)
        return results
