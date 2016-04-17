#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_grapper
----------------------------------

Tests for `grapper` module.
"""

import unittest
from grapper import grapper
import os
import json
import multiprocessing

OUTPUT_FILE = "test_output.json"


class TestGrapper(unittest.TestCase):

    def setUp(self):
        try:
            os.remove(OUTPUT_FILE)
        except OSError:
            pass

    def tearDown(self):
        try:
            os.remove(OUTPUT_FILE)
        except OSError:
            pass

    def test_file_writer(self):
        """Given a writer queue,
        When I send JSON strings to the queue,
        And I send the queue to the file writer
        Then a valid JSON list will be written 
        to the output file specified"""
        
        writer_queue = multiprocessing.Queue()
        writer_queue.put('1')
        writer_queue.put('"1"')
        writer_queue.put('{"1": 1 }')
        writer_queue.put(grapper.STOP_TOKEN)
        grapper.file_writer(OUTPUT_FILE, writer_queue, grapper.STOP_TOKEN)
        with open(OUTPUT_FILE, 'r') as output:
            jsondata = json.load(output)
            dict_list = [coord for coord in jsondata]
            self.assertEqual(dict_list, [1, "1", {"1": 1}])

    def test_remap_genome_coordinate(self):
        """Given a valid coordinate on the old reference genome,
        And a dictionary of mappings
        When I call remap_genome_coordinates
        Then I gent back the new coordinate"""
        coordinate = {"chromosome": "1", "position": 150, "reference": "A"}
        align_dict = {
            "1":(100,100,300,"2"),
            "2":(300,200,20,"7")  
        }
        new_mapping = grapper.remap_genome_coordinate(coordinate, align_dict)
        self.assertEqual(
            new_mapping, {
                "chromosome": "2", "position": 350, "reference": "A"})

    def test_remap_position_outside_expected_range(self):
        """Given a position coordinate outside of the allowed bounds for the chromosome
        And a dictionary of mappings
        When I call remap_genome_coordinates
        Then I gent back None"""
        coordinate = {"chromosome": "1", "position": 35, "reference": "A"}
        align_dict = {
            "1":(100,100,300,"2"),
            "2":(300,200,20,"7")
        }
        new_mapping = grapper.remap_genome_coordinate(coordinate, align_dict)
        self.assertEqual(new_mapping, None)
        coordinate = {"chromosome": "1", "position": 201, "reference": "A"}
        align_dict = {
            "1":(100,100,300,"2"),
            "2":(300,200,20,"7")
        }
        new_mapping = grapper.remap_genome_coordinate(coordinate, align_dict)
        self.assertEqual(new_mapping, None)

    def test_chromosome_not_mapped(self):
        """Given an input coordinate for which the chromosome is not mapped
        And a dictionary of mappings
        When I call remap_genome_coordinates
        Then I gent back None"""

        coordinate = {"chromosome": "12", "position": 150, "reference": "A"}
        align_dict = {
            "1":(100,100,300, "2"),
            "2":(300,200,20, "7")
        }
        new_mapping = grapper.remap_genome_coordinate(coordinate, align_dict)
        self.assertEqual(new_mapping, None)

    def test_handle_command(self):
        """Given the JSON alignment file
        in tests/test_data/alignment.json with contents

        [{ "length": 100,
        "source": { "chromosome": "1", "start": 100 },
        "target": { "chromosome": "2", "start": 300 } },

        { "length": 200,
        "source": { "chromosome": "2", "start": 300 },
        "target": { "chromosome": "7", "start":

        20 } }

        ]

        And the JSON source coordinate file in
        tests/test_data/source_coordinates.json with contents

        [{ "chromosome": "1", "position": 150, "reference": "A" },

         { "chromosome": "2", "position": 300, "reference": "C" }

        ]

        When I run the program

        Then I expect the JSON output file to contain target coordinates:

        [{ "chromosome": "2", "position": 350, "reference": "A" },

         { "chromosome": "7", "position": 20, "reference": "C" }

        ]
        """

        try:
            os.remove(OUTPUT_FILE)
        except OSError:
            pass
        alignfile = "tests/test_data/alignment.json"
        coordsfile = "tests/test_data/source_coordinates.json"

        grapper.handle_command(alignfile, coordsfile, OUTPUT_FILE)
        # Wait for file to be fully flushed to the disk
        with open(OUTPUT_FILE, 'r') as output:
            target_coords = json.load(output)
            dict_list = [coord for coord in target_coords]
            self.assertEqual(dict_list, [{"chromosome": "2",
                                          "position": 350,
                                          "reference": "A"},
                                         {"chromosome": "7",
                                          "position": 20,
                                          "reference": "C"}])

        os.remove(OUTPUT_FILE)

    def test_handle_outside_range_or_unmapped(self):
        """Given the JSON alignment file in
        tests/test_data/alignment.json with contents

        [{ "length": 100,
        "source": { "chromosome": "1", "start": 100 },
        "target": { "chromosome": "2", "start": 300 } },

        { "length": 200, "source": { "chromosome": "2", "start": 300 },
        "target": { "chromosome": "7", "start": 20 } }

        ]

        And the JSON source coordinate file in
        tests/test_data/source_coordinates_with_invalid.json with contents

        [{ "chromosome": "1", "position": 150, "reference": "A" },

         { "chromosome": "2", "position": 300, "reference": "C" },

         { "chromosome": "1", "position": 35, "reference": "A" },

         { "chromosome": "1", "position": 201, "reference": "A" },

         { "chromosome": "12", "position": 150, "reference": "A" }

        ]

        When I run the program

        Then I expect the JSON output file to contain target coordinates:

        [{ "chromosome": "2", "position": 350, "reference": "A" },

         { "chromosome": "7", "position": 20, "reference": "C" }



        ]
        """

        alignfile = "tests/test_data/alignment.json"
        coordsfile = "tests/test_data/source_coordinates_with_invalid.json"

        grapper.handle_command(alignfile, coordsfile, OUTPUT_FILE)
        # Wait for file to be fully flushed to the disk
        with open(OUTPUT_FILE, 'r') as output:
            target_coords = json.load(output)
            dict_list = [coord for coord in target_coords]
            self.assertEqual(dict_list, [{"chromosome": "2",
                                          "position": 350,
                                          "reference": "A"},
                                         {"chromosome": "7",
                                          "position": 20,
                                          "reference": "C"}])


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
