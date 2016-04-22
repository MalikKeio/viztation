class Reference:
    def __init__(self, string):
        self.type = None
        self.id = None
        self.entries = {}


class BibTexFile:
    def __init__(self, file):
        self._file = file
