# -*- coding: utf-8 -*-

import unittest
import os
from transclude import transclude_file, check_for_transclusion, InvalidDirectiveException, MissingFileException

from textwrap import dedent

from StringIO import StringIO

# TODO: multiline metadata

class MetadataTests(unittest.TestCase):

    def test_prefix_dashes(self):
        """There can optionally be a --- on the line before the metadata."""

        metadata = dedent("""---
            foo: bar:baz

            nometa: this
        """)

    def test_followed_by_dashes(self):
        """There can optionally be a --- on the line after the metadata."""

        metadata = dedent("""foo: bar:baz
            ---
            nometa: this
            """)

    def test_followed_by_dots(self):
        """The line after the metadata can also be ...."""

        metadata = dedent("""foo: bar:baz
            ....
            nometa: this
            """)

    def test_no_blank_line_before(self):
        """metadata must begin at the very top of the document, no blank lines can precede it."""

        metadata = dedent("""
            nometa: this
            """)

    def test_(self):
        """after the metadata is finished, a blank line triggers the beginning of the rest of the document."""

        metadata = dedent("""
        """)


    def test_(self):
        """metadata key must begin at the beginning of the line"""

        metadata = dedent("""
        """)

    def test_(self):
        """metadata key starts with an ASCII letter or a number"""

        metadata = dedent("""
        """)

    def test_(self):
        """end of the metadata key is specified with a colon (‘:’)"""

        metadata = dedent("""
        """)

    def test_(self):
        """after the colon comes the metadata value, which can consist of pretty much any characters (including new lines)."""

        metadata = dedent("""
        """)

    def test_(self):
        """Metadata keys are case insensitive and stripped of all spaces during processing."""

        metadata = dedent("""
        """)
