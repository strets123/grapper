# -*- coding: utf-8 -*-
import argparse
import ijson
import multiprocessing
import json
from os import linesep


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


def remap_genome_coordinate(coord, align_dict):
    """Given a dictionary of chromosome alignment remappings,
    remap a single coordinate"""
    original_chromosome = coord["chromosome"]
    chromosome_mapping = align_dict.get(original_chromosome, None)
    if chromosome_mapping is not None:
        source_start_point = chromosome_mapping["source"]["start"]
        bases_from_start = coord["position"] - source_start_point
        within_range = bases_from_start <= chromosome_mapping["length"]
        if bases_from_start >= 0 and within_range:
            # The base from the coordinate is within range
            new_start_point = chromosome_mapping["target"]["start"]
            new_chromosome = chromosome_mapping["target"]["chromosome"]
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
        align_dict = {item["source"]["chromosome"]: item
                      for item in alignments}
        with open(coordinate_file_path, 'r') as coordfile:
            coords = ijson.items(coordfile, 'item')
            for index, coord in enumerate(coords):
                data_dict = remap_genome_coordinate(coord, align_dict)
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
