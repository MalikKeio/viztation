import logging

def getEntry(string):
    """
    Get a stripped reference entry as argument
    Like 'author="Newton, Isaac"' for example.
    """
    logging.debug("Entry:", string, "EOS")
    equal = string.find("=")
    if equal == -1:
        name = None
        content = None
    else:
        first_dquote = string.find('"', equal)
        first_curly = string.find('{', equal)
        name = string[0:equal].strip()
        logging.debug("getEntry: first_dquote=%d, first curly=%d" % (first_dquote, first_curly))
        if first_curly == -1 or (first_dquote != -1 and first_dquote < first_curly):
            # Found "", look for the next dquote
            last_dquote = string.rfind('"')
            content = string[first_dquote+1:last_dquote]
        elif first_dquote == -1 or (first_curly != -1 and first_curly < first_dquote):
            # Did not found "", the user may be using {}
            last_curly = string.rfind('}')
            content = string[first_curly+1:last_curly]
    return name, content

class Reference:
    def __init__(self, string):
        string = string.strip()
        logging.debug(string + "\n\n")
        last_curly = string.rfind('}')
        cursor = 0
        if len(string) == 0 or string[0] != "@":
            logging.error("Did not found expected `@` at beginning of reference.\n" + string)
            self._error_handler()
        else:
            first_curly = string.find('{')
            if first_curly == -1:
                logging.error("Did not found expected `{` after reference type.\n" + string)
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
                first_curly = string.find('{', cursor)
                logging.debug("first_dquote=%d, first curly=%d" % (first_dquote, first_curly))
                if first_curly == -1 and first_dquote == -1:
                    logging.error("No '\"' nor '{' were found.\n" + string)
                    return
                if first_curly == -1 or (first_dquote != -1 and first_dquote < first_curly):
                    # Found "", look for the next dquote
                    logging.debug('Use ""')
                    next_dquote = string.find('"', first_dquote + 1)
                    next_comma = string.find(',', next_dquote + 1)
                    has_entry = next_comma != -1
                    if has_entry:
                        entry_substring = string[cursor:next_comma].strip()
                    else:
                        entry_substring = string[cursor:last_curly].strip()
                    cursor = next_comma + 1
                elif first_dquote == -1 or (first_curly != -1 and first_curly < first_dquote):
                    # Did not found "", the user may be using {}
                    logging.debug("Use {}")
                    curly_counter = 0
                    last_curly_index = -1
                    start_type = cursor
                    while cursor < len(string) and last_curly_index < 0:
                        if string[cursor] == "{":
                            curly_counter += 1
                        elif string[cursor] == "}":
                            curly_counter -= 1
                            if curly_counter == 0:
                                last_curly_index = cursor
                        cursor += 1
                    next_comma = string.find(',', last_curly_index + 1)
                    has_entry = next_comma != -1
                    entry_substring = string[start_type:last_curly_index+1].strip()
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
    def __init__(self, filename):
        self.filename = filename
        f = open(filename, 'r')
        content = f.read()
        print(content)
        cursor = 0
        curly_counter = 0
        last_curly_index = -1
        self.references = []
        has_reference = True
        while cursor < len(content):
            cursor_start = cursor
            while cursor < len(content) and last_curly_index < 0:
                if content[cursor] == "{":
                    curly_counter += 1
                elif content[cursor] == "}":
                    curly_counter -= 1
                    if curly_counter == 0:
                        last_curly_index = cursor
                cursor += 1
            reference_string = content[cursor_start:cursor]
            if len(reference_string) > 0:
                self.references.append(Reference(reference_string))
            cursor += 1
            last_curly_index = -1
