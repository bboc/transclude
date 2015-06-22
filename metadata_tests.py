# -*- coding: utf-8 -*-

import unittest
import os
from transclude import transclude_file, check_for_transclusion, InvalidDirectiveException, MissingFileException

from textwrap import dedent

from StringIO import StringIO

from metadata import read_metadata


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

    def test_metadata_key_at_line_start(self):
        """metadata key must begin at the beginning of the line"""
        metadata = read_metadata(StringIO(dedent(""" this is not metadata.
            nometa: this
            """)))
        self.assertEqual(metadata, {})
        self.assertFalse(metadata.has_key('nometa'))

    def test_metadata_key_first_character_is_alnum(self):
        """metadata key starts with an ASCII letter or a number"""
        metadata = read_metadata(StringIO(dedent("""\
            wharrgarbl:this is metadata.
            """)))
        self.assertEqual(metadata, {'wharrgarbl': 'this is metadata.'})
        metadata = read_metadata(StringIO(dedent("""\
            2be or not 2 be:this is also metadata.
            """)))
        self.assertEqual(metadata, {'2beornot2be': 'this is also metadata.'})
        metadata = read_metadata(StringIO(dedent("""\
            -: this is not metadata.
            nometa: this
            """)))
        self.assertEqual(metadata, {})
        self.assertFalse(metadata.has_key('nometa'))
        

class MetadataKeyValueTests(unittest.TestCase):

    def test_keys_are_lowercased_and_stripped_of_spaces(self):
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

    def test_multiline_values(self):
        """after the colon comes the metadata value, which can consist of pretty much any characters (including new lines)."""
        """multiline metadata values are processed correctly."""
        """If your metadata value includes a colon, it must be indented to keep it from being treated as a new key-value pair."""
        source = StringIO(dedent("""\
            multiline-key:This is the text of the first line of the key,
            and this is the second line of the key.
                funny enough, there's also a third line with some intentation.
            simple-key:justoneword
            another multiline key:here we go
                with another line with a colon: yay

            nometa: this
        """))
        metadata = read_metadata(source)
        self.assertDictContainsSubset(
            {'multiline-key': dedent("""\
                This is the text of the first line of the key,
                and this is the second line of the key.
                    funny enough, there's also a third line with some intentation."""),
             'simple-key': 'justoneword',
             'anothermultilinekey': dedent("""\
                here we go
                    with another line with a colon: yay""")
             },
            metadata, 
            #repr(metadata)
            )

