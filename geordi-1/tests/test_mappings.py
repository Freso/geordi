#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright 2013 MetaBrainz Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import re
import geordi.mappings

class TestMappings(unittest.TestCase):

    def test_code_url(self):
        urls = []
        for (idx, cls) in geordi.mappings.class_map.iteritems():
            self.assertTrue(cls.code_url() not in urls,
                            msg="Code URL must be different for each index")
            urls.append(cls.code_url())

            self.assertTrue(re.search('geordi/mappings/{0}.py'.format(idx),
                                      cls.code_url()),
                            msg="Mapping class and file are named the same")

            self.assertTrue(cls.code_url(),
                            msg="Code URL must be available for all mappings.")

    def test_link_types(self):
        for (idx, cls) in geordi.mappings.class_map.iteritems():
            self.assertTrue('version' in cls.link_types())

    def test_map(self):
        for (idx, cls) in geordi.mappings.class_map.iteritems():
            self.assertTrue(callable(cls.map),
                            msg="All mappings must have a map function")

    def test_automatic_matches(self):
        for (idx, cls) in geordi.mappings.class_map.iteritems():
            self.assertTrue(callable(cls.automatic_item_matches))
            self.assertTrue(callable(cls.automatic_subitem_matches))

    def test_get_mapoptions(self):
        everything_track = {
            'medium': ['1'],
            'totaltracks': ['50'],
            'acoustid': ['a644724e-db4f-4885-a6b3-c86b52d2e7da']
        }
        nothing_track = {
            'medium': [],
            'totaltracks': [],
            'acoustid': []
        }
        partial_track = {
            'medium': nothing_track['medium'],
            'totaltracks': nothing_track['totaltracks'],
            'acoustid': everything_track['acoustid']
        }

        self.assertEqual(geordi.mappings.get_mapoptions({
            'release': {'tracks': [everything_track, nothing_track]}
        }), {
            'mediums': True,
            'totaltracks': True,
            'acoustid': True
        }, msg="everything + nothing -> everything")

        self.assertEqual(geordi.mappings.get_mapoptions({
            'release': {'tracks': [partial_track, everything_track]}
        }), {
            'mediums': True,
            'totaltracks': True,
            'acoustid': True
        }, msg="partial + everything -> everything")

        self.assertEqual(geordi.mappings.get_mapoptions({
            'release': {'tracks': [nothing_track, nothing_track]}
        }), {
            'mediums': False,
            'totaltracks': False,
            'acoustid': False
        }, msg="nothing in, nothing out")

        self.assertEqual(geordi.mappings.get_mapoptions({
            'release': {'tracks': [partial_track, nothing_track]}
        }), {
            'mediums': False,
            'totaltracks': False,
            'acoustid': True
        }, msg="partial track -> partial map options")
