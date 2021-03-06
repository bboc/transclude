# -*- coding: utf-8 -*-

"""
transclude multimarkdown files.
"""

from __future__ import print_function

import os
import os.path
from metadata import read_metadata


def transclude(source_path, target_path, output_type):
    """Transclude source to target, use output_type for wildcards."""
    with file(target_path, 'w+') as target:
        transclude_file(source_path, target, output_type)


def transclude_file(source_path, target, output_type):
    sf = TranscludeRoot(source_path, target, output_type)
    sf.transclude()


class MissingFileException(Exception):
    pass


class TranscludeFile(object):

    def __init__(self, source_path, target, output_type):
        self.source_path = source_path
        self.target = target
        self.type = output_type

        self.source = file(self.source_path, 'r')
        self.transcludebase = os.path.dirname(source_path)

        self.metadata = read_metadata(self.source)

    def transclude(self):
        while True:
            line = self.source.readline()
            if line == '':
                break
            try:
                found, data = check_for_transclusion(line)
            except InvalidDirectiveException, e:
                raise InvalidDirectiveException(e[0], self.source_path)
            if found:
                prefix, next_filename, offset = data
                self.target.write(prefix)

                if next_filename.endswith('*'):
                    next_filename = next_filename[:-1] + self.type

                next_file = os.path.join(
                    self.transcludebase, next_filename)

                if not os.path.exists(next_file):
                    raise MissingFileException(
                        self.source_path, next_filename, os.getcwd())

                tf = TranscludeFile(next_file,
                                    self.target,
                                    self.type)
                tf.transclude()
                self.source.seek(-(len(line) - offset), os.SEEK_CUR)

            else:
                self.target.write(line)


class TranscludeRoot(TranscludeFile):

    """The root TranscludeFile sets transcludebase to file's basepath and 
    processes metadata 'transcludebase'."""

    def __init__(self, source_path, target, output_type):
        """Set transcludebase."""
        super(TranscludeRoot, self).__init__(
            source_path, target, output_type)
        self.source.seek(0)  # rewind to include metadata of root file
        if self.metadata.has_key('transcludebase'):
            self.transcludebase = os.path.join(
                self.transcludebase, self.metadata['transcludebase'].strip())


class InvalidDirectiveException(Exception):
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

        return True, (line[:start], line[start + 2:end], end + 2)


def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser(
        description='transclude source markdown file to target file.')
    parser.add_argument('source_path',
                        help='path to the source file')
    parser.add_argument('output',
                        help='path to the output file')
    parser.add_argument('--type', default='md',
                        choices=[
                            'md', 'latex', 'html', 'lyx', 'opml', 'rtf', 'odf'],
                        help='file type for wildcard transclusion (default: md)')

    args = parser.parse_args()
    try:
        transclude(args.source_path, args.output, args.type)
    except MissingFileException, e:
        print('ERROR: missing', e[0], 'in file', e[
              1], 'current working directory:', e[2], file=sys.stderr)
        sys.exit(1)
    except InvalidDirectiveException, e:
        print ('ERROR: broken transclude directive in', e[1], file=sys.stderr)
        print ('offending line:: ', e[0], file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
