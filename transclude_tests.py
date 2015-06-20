# -*- coding: utf-8 -*-

import unittest
import os
from transclude import transclude_file, check_for_transclusion, InvalidDirectiveException, DuplicateDirectiveException
from tempfile import NamedTemporaryFile
import filecmp
from difflib import context_diff


def make_path(file_name):
    test_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'test-data')
    return os.path.join(test_dir, file_name)


class BasicTranscludeTests(unittest.TestCase):

    def setUp(self):
        """Create tempfile as target, add cleanup methods to close and unlink tempfiles."""
        self.target = NamedTemporaryFile(delete=False)
        self.addCleanup(self.target.close)
        self.addCleanup(os.unlink, self.target.name)

    def compare_results(self, correct_path):
        """Compare the actual result with the correct result."""
        with file(correct_path, 'r+') as correct:
            c = correct.readlines()
            self.target.seek(0)
            t = self.target.readlines()
            self.assertEqual(c, t)

    def test_no_transclusion(self):
        """Transcluding a file without transclude directive returns the original file."""
        transclude_file(make_path("no-transclusion.md"), self.target, 'md')
        self.compare_results(make_path("no-transclusion.md"))

    def test_simple_transclude(self):
        """Transclude replaces directive {{some_other_file.txt}} with contents of some_other_file.txt."""
        """transclude looks for files in parent folder of source"""
        transclude_file(make_path("simple-transclusion.md"), self.target, 'md')
        self.compare_results(make_path("simple-transclusion-result.md"))

    def test_recursive_transclude(self):
        """Transclude is recursive."""
        transclude_file(make_path("recursive-transclusion.md"), self.target, 'md')
        self.compare_results(make_path("recursive-transclusion-result.md"))

    def test_two_transclusions_in_one_line(self):
        """Two transclusion directives in one file are handled correctly."""
        transclude_file(make_path("double-transclusion.md"), self.target, 'md')
        self.compare_results(make_path("double-transclusion-result.md"))



"""Transclude stops on recursive loop."""

"""transclude outputs an error when a file to transclude is not found."""

"""Wildcard transclusion {{foo.*}} wildcard is set according to type (tex, html, )"""

"""Transclude ignores metadata in transculded file."""


"""with recursion, transclude looks for files relative to the file which transludes them."""

"""after recursion, transclude looks for files again relative to source."""

"""if metadata "Transclude Base" is set, transclude looks there for files."""


class FindDirectiveTests(unittest.TestCase):

    def test_no_directive(self):

        result = check_for_transclusion("this line has no directive")
        self.assertEqual(result, (False, None))

    def test_one_directive(self):
        result = check_for_transclusion(
            'this line has one directive {{yay/foobar.md}}')
        self.assertEqual(
            result, (True, ('this line has one directive ', 'yay/foobar.md', 45)))

    def test_incomplete_directive_raises_exception(self):
        self.assertRaises(InvalidDirectiveException, check_for_transclusion,
                          'this line has a directive }}{{yay/foobar.md}}')

    def test_second_directive_raises_exception(self):
        self.assertRaises(DuplicateDirectiveException, check_for_transclusion,
                          'this line has two directives {{yay/foobar.md}} some text {{anotherone.md}}')

    def test_seek_offset_is_calculated_properly(self):
        result = check_for_transclusion(
            'this line has a directive {{yay/foobar.md}} and 19 characters.')
        self.assertEqual(
            result, (True, ('this line has a directive ', 'yay/foobar.md', 43)))

