import re

from lib import audit


class Audit(audit.Auditor):

    @property
    def regex_word(self) -> str:
        return r'(\s|\")([0-9]|[a-z]|[A-Z]){32,128}( |\"|$)'

    def extend_filter(self, result) -> list:
        hits: list = []
        for line in result:
            hit: str = ""
            if "private" in line.lower():
                hit = line
            elif "token" in line.lower():
                hit = line
            elif "secret" in line.lower():
                hit = line
            filename = line.split(":")[0]
            payload = ":".join(line.split(":")[1:])
            if len(payload) > 256:
                repattern = re.compile(self.regex_word)
                hit_p = repattern.search(line)
                if hit_p:
                    prefix = filename + (" [Because of longer line omit "
                                         "line with matched word.]: ")
                    hit = prefix + hit_p.group(0)
            hits.append(hit)
        return hits
