# -*- coding: utf-8 -*-


def read_metadata(source_file):
    """Read metadata from source file.

    Return a dictionary with the metadata, set the file seek pointer to 
    the first character after the metadata.
    """
    metadata = {}
    first = True
    while True:
        line = source_file.readline().rstrip()
        if first:
            first = False
            if line == '':
                # no metadata
                source_file.seek(0)
                break
            elif line == '---':
                # begin metadata
                continue
            elif not line[0].isalnum() or line.find(':') == -1:
                # no metadata: seek zero and return
                source_file.seek(0)
                break
        else:
            if line in ['', '---', '...']:
                # end of metadata
                break

        # extract key or append value
        if not line[0].isalnum() or line.find(':') == -1:
            # multiline value, append to previous value
            metadata[key] = '\n'.join((metadata[key], line))
        else:
            # create new key
            pos = line.find(':')
            key = line[:pos].replace(' ', '').lower()
            value = line[pos + 1:]
            metadata[key] = value
    return metadata
