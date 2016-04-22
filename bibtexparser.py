import logging

def getEntry(string):
    """
    Get a stripped reference entry as argument
    Like 'author="Newton, Isaac"' for example.
    """
    print("Entry:", string, "EOS")
    equal = string.find("=")
    if equal == -1:
        name = None
        content = None
    else:
        first_dquote = string.find('"', equal)
        name = string[0:equal].strip()
        if first_dquote != -1:
            # Found "", look for the next dquote
            next_dquote = string.rfind('"')
            content = string[first_dquote+1:next_dquote]
        else:
            # Did not found "", the user may be using {}
            entry_substring = ""
            raise "Not implemented"
    return name, content

class Reference:
    def __init__(self, string):
        string = string.strip()
        last_curly = string.rfind('}')
        cursor = 0
        if string[0] != "@":
            logging.error("Did not found expected `@` at beginning of reference.")
            self._error_handler()
        else:
            first_curly = string.find('{')
            if first_curly == -1:
                logging.error("Did not found expected `{` after reference type.")
                self._error_handler()
                return
            self.type = string[1:first_curly].strip()
            end_of_id = string.index(',', first_curly)
            self.id = string[first_curly + 1:end_of_id].strip()
            cursor = end_of_id + 1
            # Dealing with entries
            # Loop ending condition: no "," found
            self.entries = {}
            has_entry = True
            while has_entry:
                first_dquote = string.find('"', cursor)
                if first_dquote != -1:
                    # Found "", look for the next dquote
                    next_dquote = string.find('"', first_dquote + 1)
                    next_comma = string.find(',', next_dquote + 1)
                    has_entry = next_comma != -1
                    if has_entry:
                        entry_substring = string[cursor:next_comma].strip()
                    else:
                        entry_substring = string[cursor:last_curly].strip()
                    cursor = next_comma + 1
                else:
                    # Did not found "", the user may be using {}
                    curly_counter = 0
                    first_curly_index = -1
                    last_curly_index = -1
                    while cursor < len(string) and (last_curly_index < 0 or first_curly_index < 0):
                        if string[cursor] == "{":
                            curly_counter += 1
                            first_curly_index = cursor
                        elif string[cursor] == "}":
                            curly_counter -= 1
                            if curly_counter == 0:
                                last_curly_index = cursor
                        cursor += 1
                    next_comma = string.find(',', last_curly_index + 1)
                    has_entry = next_comma != -1
                    entry_substring = string[first_curly_index:last_curly_index+1].strip()
                    cursor = next_comma + 1
                # First entry may be empty if bibtex has an empty reference
                if entry_substring == "":
                    has_entry = False
                else:
                    name, content = getEntry(entry_substring)
                    self.entries[name] = content

    def _error_handler(self):
        self.type = None
        self.id = None
        self.entries = {}


class BibTexFile:
    def __init__(self, file):
        self._file = file
