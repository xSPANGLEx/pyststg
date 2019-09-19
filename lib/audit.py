import glob
import importlib

from lib import git


class Auditor(object):

    def __init__(self, repository) -> None:
        self.repository = repository

    def extend_filter(self, result) -> list:
        return result

    @property
    def regex_word(self) -> str:
        raise NotImplementedError()

    def audit(self) -> list:
        result = self.repository.grep(self.regex_word)
        return self.extend_filter(result)


class Audit(object):

    def __init__(self, repository):
        self.repository = git.Git(repository)

    def execute(self):
        modules = [
                name.split(".py")[0].replace("/", ".")
                for name in glob.glob("patterns/*")
                if name.endswith(".py")
                ]
        auditors = [
                importlib.import_module(module)
                for module in modules
                ]
        results = set()
        for auditor in auditors:
            result = auditor.Audit(self.repository).audit()
            for line in result:
                results.add(line)
        return list(results)
