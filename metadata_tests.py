# -*- coding: utf-8 -*-

import unittest
import os
from transclude import transclude_file, check_for_transclusion, InvalidDirectiveException, MissingFileException

from textwrap import dedent

from StringIO import StringIO

from metadata import read_metadata

# TODO: multiline metadata
# TODO: check file seek pointer in each section test


class MetadataSectionTests(unittest.TestCase):

    def test_prefix_dashes(self):
        """There can optionally be a --- on the line before the metadata."""

        source = StringIO(dedent("""\
            ---
            foo:bar:baz

            nometa: this
        """))
        metadata = read_metadata(source)
        self.assertDictContainsSubset(
            {'foo': 'bar:baz'}, metadata, repr(metadata))
        self.assertFalse(metadata.has_key('nometa'))
        self.assertEqual('nometa: this\n', source.readline())

    def test_followed_by_dashes(self):
        """There can optionally be a --- on the line after the metadata."""

        source = StringIO(dedent("""\
            foo:bar:baz
            ---
            nometa: this
            """))
        metadata = read_metadata(source)
        self.assertDictContainsSubset(
            {'foo': 'bar:baz'}, metadata, repr(metadata))
        self.assertFalse(metadata.has_key('nometa'))
        self.assertEqual('nometa: this\n', source.readline())

    def test_followed_by_dots(self):
        """The line after the metadata can also be ..."""

        source = StringIO(dedent("""\
            foo:bar:baz
            ...
            nometa: this
            """))
        metadata = read_metadata(source)
        self.assertDictContainsSubset(
            {'foo': 'bar:baz'}, metadata, repr(metadata))
        self.assertFalse(metadata.has_key('nometa'))
        self.assertEqual('nometa: this\n', source.readline())        

    def test_(self):
        """after the metadata is finished, a blank line triggers the beginning of the rest of the document."""

        source = StringIO(dedent("""\
            foo:bar:baz

            nometa: this
        """))
        metadata = read_metadata(source)
        self.assertDictContainsSubset(
            {'foo': 'bar:baz'}, metadata, repr(metadata))
        self.assertFalse(metadata.has_key('nometa'))
        self.assertEqual('nometa: this\n', source.readline())        

    def test_no_blank_line_before(self):
        """metadata must begin at the very top of the document, no blank lines can precede it."""

        source = StringIO(dedent("""\

            nometa: this
            """))
        metadata = read_metadata(source)
        self.assertEqual(metadata, {})
        self.assertFalse(metadata.has_key('nometa'))
        self.assertEqual('\n', source.readline())

    def test_seek_to_zero_if_first_line_has_no_key(self):
        source = StringIO(dedent("""\
            this is not metadata.

            nometa: this
            """))
        metadata = read_metadata(source)
        self.assertEqual(metadata, {})
        self.assertFalse(metadata.has_key('nometa'))
        self.assertEqual('this is not metadata.\n', source.readline())


class MetadataKeyValueTests(unittest.TestCase):

    """metadata key must begin at the beginning of the line"""
    """metadata key starts with an ASCII letter or a number"""
    """after the colon comes the metadata value, which can consist of pretty much any characters (including new lines)."""

    def test_(self):
        """Metadata keys are case insensitive and stripped of all spaces during processing."""

        source = StringIO(dedent("""\
            this is one key:first
            tHis IsAno th   ER:second

            nometa: this
        """))
        metadata = read_metadata(source)
        self.assertDictContainsSubset(
            {'thisisonekey': 'first',
             'thisisanother': 'second'},
            metadata, repr(metadata))
