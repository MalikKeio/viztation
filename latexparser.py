import re



class LaTexFile:
    unknown_count = 0
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
        title_index = content.find(r'\title')
        if title_index == -1:
            self.title = "Unknown paper %d" % LaTexFile.unknown_count
            LaTexFile.unknown_count += 1
        else:
            right_curly_index = -1
            curly_count = 0
            left_curly_index = content.find('{', title_index)
            cursor = left_curly_index
            while cursor < len(content) and right_curly_index < 0:
                if content[cursor] == '{':
                    curly_count += 1
                elif content[cursor] == '}':
                    curly_count -= 1
                    if curly_count == 0:
                        right_curly_index = cursor
                cursor += 1
            if right_curly_index >= 0:
                self.title = content[left_curly_index+1:right_curly_index].strip()
            else:
                self.title = "Unknown paper %d" % LaTexFile.unknown_count
                LaTexFile.unknown_count += 1


    def __str__(self):
        return self.title

class LaTexFiles:
    def __init__(self, filenames):
        self.files = [LaTexFile(filename) for filename in filenames]
