import re

class LaTexFile:
    def __init__(self, filename):
        f = open(filename, 'r')
        content = f.read()
        f.close()
        self.cites = re.findall(r'\\cite{(\w+)}', content)
