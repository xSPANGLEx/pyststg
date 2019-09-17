import shutil

from git import Repo, cmd  # type: ignore

WORKDIR_PREFIX = "/tmp/pyststg-"


class Git(object):

    def __init__(self, repository: str) -> None:
        self._id: str = str(id(self))
        self.workdir: str = WORKDIR_PREFIX + self._id
        self.repository: Repo = Repo.clone_from(
                repository, self.workdir, branch="master")

    def grep(self, word) -> list:
        repository: cmd.Git = cmd.Git(self.workdir)
        revs: str = repository.rev_list("--all")
        hits: set = set()
        for rev in revs.split("\n"):
            try:
                result: str = repository.grep("-E", word, rev)
                hit: list = result.split("\n")
                for line in hit:
                    line = ":".join(line.split(":")[1:])
                    hits.add(line)
            except Exception:
                pass
        return list(hits)

    def close(self) -> None:
        self.__del__()

    def get_branches(self) -> list:
        return self.repository.branches

    def checkout(self, branch: str) -> None:
        self.repository.git.checkout(branch)

    def __del__(self) -> None:
        shutil.rmtree(self.workdir, ignore_errors=True)
