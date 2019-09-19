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
        _id = self.repository.run(self.regex_word)
        self.repository.join(_id)
        result = self.repository.get_result(_id)
        return self.extend_filter(result)


class Audit(object):

    def __init__(self, repository):
        self.repository = git.Git(repository)

    def execute(self) -> list:
        modules = [
                name.split(".py")[0].replace("/", ".")
                for name in glob.glob("patterns/*")
                if name.endswith(".py")
                ]
        auditors = [
                importlib.import_module(module)
                for module in modules
                ]
        results: set = set()
        for auditor in auditors:
            result = auditor.Audit(self.repository).audit()  # type: ignore
            for line in result:
                results.add(line)
        return list(results)
