import re

class LaTexFile:
    def __init__(self, filename):
        f = open(filename, 'r')
        content = f.read()
        f.close()
        cites = re.findall(r'\\cite{([\w,]+)}', content)
        nocites = re.findall(r'\\nocite{([\w,]+)}', content)
        self.cites = []
        for cite in cites:
            self.cites.extend(cite.split(','))
        for nocite in nocites:
            self.cites.extend(nocite.split(','))
