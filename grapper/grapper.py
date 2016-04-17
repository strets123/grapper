# -*- coding: utf-8 -*-
import argparse
import ijson
import multiprocessing
import json
from os import linesep
from bisect import bisect_left

STOP_TOKEN = "STOP!!!"


def file_writer(dest_filename, some_queue, some_stop_token):
    """Write JSON strings to a JSON list from a multiprocessing
    queue to a file until the stop token is sent"""
    is_start_of_json = True
    with open(dest_filename, 'w') as dest_file:
        dest_file.write("[")
        while True:
            line = some_queue.get()
            if line == some_stop_token:
                dest_file.write(linesep)
                dest_file.write("]")
                return
            if is_start_of_json:
                is_start_of_json = False
            else:
                dest_file.write(",")
                dest_file.write(linesep)
            dest_file.write(line)


def remap_genome_coordinate(coord, align_tuples, startpoints):
    """Given a tuple of chromosome alignment remappings,
    remap a single coordinate"""
    original_chromosome = coord["chromosome"]
    # The bisect left function gives the nearest item in the array
    # If the items are equal, in this case we want them to be part of
    # The same mapping so we add 1
    ind = bisect_left(startpoints, (coord["position"] + 1)) -1
    if ind == -1:
        #The coordinate is before the first chromosome
        return None
    chromosome_mapping = align_tuples[ind]
    (source_start_point,
     source_chromosome,
     length, 
     new_start_point, 
     new_chromosome) = chromosome_mapping

    if original_chromosome == source_chromosome:
        bases_from_start = coord["position"] - source_start_point
        within_range = bases_from_start <= length
        if bases_from_start >= 0 and within_range:
            # The base from the coordinate is within range
            coord["chromosome"] = new_chromosome
            coord["position"] = new_start_point + bases_from_start
            return coord
    return None


def remap_reference_genome(alignment_file_path,
                           coordinate_file_path,
                           writer_queue):
    """Given the file path to an alignment file and the
    file path to a coordinate file
    write an output file which maps
    the source genome coordinates to a new reference genome"""
    with open(alignment_file_path, 'r') as align:
        alignments = ijson.items(align, 'item')
        align_tuples = [(item["source"]["start"],
                       item["source"]["chromosome"],
                       item["length"],
                       item["target"]["start"],
                       item["target"]["chromosome"])
                      for item in alignments]
        align_tuples.sort(key=lambda tup: tup[0])
        startpoints = [tup[0] for tup in align_tuples]
        with open(coordinate_file_path, 'r') as coordfile:
            coords = ijson.items(coordfile, 'item')
            for index, coord in enumerate(coords):
                data_dict = remap_genome_coordinate(coord, align_tuples, startpoints)
                if data_dict is not None:
                    writer_queue.put(json.dumps(data_dict))


def get_writer_process_and_queue(output):
    """Returns a multiprocessing process to write to a
     file and a queue to do the writing"""
    queue = multiprocessing.Queue()
    return (
        multiprocessing.Process(
            target=file_writer,
            args=(
                output,
                queue,
                STOP_TOKEN)),
        queue)


def handle_command(alignfile, coordsfile, output):
    """Given alignfile, coordsfile and output file paths, remap a genome"""
    writer_process, writer_queue = get_writer_process_and_queue(output)
    writer_process.start()
    remap_reference_genome(alignfile, coordsfile, writer_queue)
    writer_queue.put(STOP_TOKEN)
    writer_process.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("alignfile", help="Path to the alignment JSON file")
    parser.add_argument("coordsfile", help="Path to the coordinates JSON file")
    parser.add_argument("output", help="Path to the desired output file")
    args = parser.parse_args()
    handle_command(args.alignfile, args.coordsfile, args.output)
