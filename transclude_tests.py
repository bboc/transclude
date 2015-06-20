# -*- coding: utf-8 -*-

import unittest
import os
from transclude import transclude_file
from tempfile import NamedTemporaryFile
import filecmp
from difflib import context_diff

def make_path(file_name):
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-data')
    return os.path.join(test_dir, file_name)    


class BasicTranscludeTests(unittest.TestCase):

    def setUp(self):

        self.target = NamedTemporaryFile(delete=False)

        self.addCleanup(self.target.close)
        self.addCleanup(os.unlink, self.target.name)

    def test_not_transclusion(self):
        """Transcluding a file without transclude directive returns the original file."""

        transclude_file(make_path("no-transclusion.md"), self.target, 'md')
        self.compare_results(make_path("no-transclusion.md"))


    def compare_results(self, correct_path):
        with file(correct_path, 'r+') as correct:

            c = correct.readlines()
            self.target.seek(0)
            t = self.target.readlines()
            self.assertEqual(c, t)
    

"""Transclude replaces directive {{some_other_file.txt}} with contents of some_other_file.txt."""

"""Transclude is recursive."""

"""Transclude stops on recursive loop."""

"""transclude outputs an error when a file to transclude is not found."""

"""Wildcard transclusion {{foo.*}} wildcard is set according to type (tex, html, )"""

"""Transclude ignores metadata in transculded file."""

"""transclude looks for files in parent folder of source"""

"""with recursion, transclude looks for files relative to the file which transludes them."""

"""after recursion, transclude looks for files again relative to source."""

"""if metadata "Transclude Base" is set, transclude looks there for files."""

