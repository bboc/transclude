# -*- coding: utf-8 -*-

"""
transclude multimarkdown files

"""

def transclude(source_path, target_path, output_type):
    """Transclude source to target, use output_type for wildcards."""
    with file(target_path, 'w+') as target: 
        transclude_file(source_path, target, output_type, True)


def transclude_file(source_path, target, output_type):
    sf = TranscludeRoot(source_path, target, output_type)
    sf.transclude()

class TranscludeFile(object):

    def __init__(self, source_path, target, output_type):
        self.type = output_type
        self.source_path = source_path
        self.target = target

    def transclude(self): 
        with file(self.source_path, 'r') as self.source: 
            self.read_metadata()
            transclude_base = self.transclude_base()
            for line in self.source:
                self.target.write(line)

    def read_metadata(self):
        self.metadata = {}

    def transclude_base(self):
        return ''



class TranscludeRoot(TranscludeFile):
    """First TranscludeFile processes metadata 'transcludebase'."""

    def transclude_base(self):
        return self.metadata.get("transcludebase", None)



def main():
    pass

if __name__ == '__main__':
    pass
