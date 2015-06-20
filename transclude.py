# -*- coding: utf-8 -*-

"""
transclude multimarkdown files

"""

import os, os.path

def transclude(source_path, target_path, output_type):
    """Transclude source to target, use output_type for wildcards."""
    with file(target_path, 'w+') as target:
        transclude_file(source_path, target, output_type)


def transclude_file(source_path, target, output_type):
    sf = TranscludeRoot(source_path, target, output_type)
    sf.transclude()


class TranscludeFile(object):

    def __init__(self, source_path, target, output_type, transcludebase):
        self.type = output_type
        self.source_path = source_path
        self.target = target
        self.transcludebase = transcludebase

    def transclude(self):
        with file(self.source_path, 'r') as self.source:
            # TODO read/skip metadata here
            for line in self.source:

                found, data = check_for_transclusion(line)
                if found:
                    prefix, next_filename, offset = data
                    self.target.write(prefix)
                    tf = TranscludeFile(os.path.join(self.transcludebase, next_filename), 
                                        self.target, 
                                        self.type,
                                        self.transcludebase)
                    tf.transclude()
                    self.target.write(line[offset:])
                    # TODO: write rest of line here
                else:
                    self.target.write(line)


class TranscludeRoot(TranscludeFile):
    """The root TranscludeFile sets transcludebase to file's basepath and 
    processes metadata 'transcludebase'."""

    def __init__(self, source_path, target, output_type):
        """Set transcludebase."""
        transcludebase = os.path.dirname(source_path)
        super(TranscludeRoot, self).__init__(source_path, target, output_type, transcludebase)


class InvalidDirectiveException(Exception):
    pass


class DuplicateDirectiveException(Exception):
    pass


def check_for_transclusion(line):
    """Test if a line contains a transclusion. 

    Return tuple (found, data)
    found is True when a transclude directive has been found
    data is tuple (prefix, filename, seek_offset) or none
    prefix is the string which prefixes the transclude directive,full line if none was found
    filename is the contents of the transclude directive, None if the line contains no directive.
    seek_offset: is the offset to the position immediately after transclude directive 
    """
    start = line.find('{{')
    if start == -1:
        return False, None
    else:
        end = line.find('}}')
        if end < start:
            raise InvalidDirectiveException(line)

        if line.find('{{', end) != -1:
            raise DuplicateDirectiveException(line)

        return True, (line[:start], line[start + 2:end], end+2)


def main():
    pass

if __name__ == '__main__':
    pass
