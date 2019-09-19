import queue
import shutil
import threading

from git import Repo, cmd  # type: ignore

WORKDIR_PREFIX = "/tmp/pyststg-"


class Git(object):

    def __init__(self, repository: str, worker_num=16) -> None:
        self._id: str = str(id(self))
        self.workdir: str = WORKDIR_PREFIX + self._id
        self.repository: Repo = Repo.clone_from(
                repository, self.workdir, branch="master")
        self.global_queue: dict = {}
        self.global_hits: dict = {}
        self.worker_num = worker_num
        self.global_workers: dict = {}
        self.id_counter = 0

    def worker(self, _id):
        repository: cmd.Git = cmd.Git(self.workdir)
        while 1:
            target = self.global_queue[_id].get()
            if target is None:
                break
            rev, word = target
            try:
                result: str = repository.grep("-E", word, rev)
            except Exception:
                continue
            hit: list = result.split("\n")
            for line in hit:
                line = ":".join(line.split(":")[1:])
                self.global_hits[_id].add(line)

    def run(self, word: str) -> int:
        _id = int(self.id_counter)
        self.id_counter += 1
        workers = []
        self.global_queue[_id] = queue.Queue()
        self.global_hits[_id] = set()
        for i in range(self.worker_num):
            th = threading.Thread(target=self.worker, args=(_id,))
            th.setDaemon(True)
            th.start()
            workers.append(th)
        self.global_workers[_id] = workers
        repository: cmd.Git = cmd.Git(self.workdir)
        revs: str = repository.rev_list("--all")
        for rev in revs.split("\n"):
            self.global_queue[_id].put((rev, word))
        for i in range(self.worker_num):
            self.global_queue[_id].put(None)
        return _id

    def join(self, _id):
        for worker in self.global_workers[_id]:
            worker.join()

    def get_result(self, _id) -> list:
        return list(self.global_hits[_id])

    def get_branches(self) -> list:
        return self.repository.branches

    def checkout(self, branch: str) -> None:
        self.repository.git.checkout(branch)

    def __del__(self) -> None:
        shutil.rmtree(self.workdir, ignore_errors=True)
