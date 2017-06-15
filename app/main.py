#!/usr/bin/python

"""
author: Lukasz Dynowski
email: ludd@cbs.dtu.dk
licence: MIT
"""
import os
import json
import time
import argparse
from src.statistics import Statistic


parser = argparse.ArgumentParser(description='Program extracts statistical data from fsa file')
parser.add_argument('file_path', metavar='file_path', type=str, nargs='+', help='Path to fsa file')

DATA_FILE = None
FILE_PATH = parser.parse_args().file_path[0]

try:
    assert os.path.exists(FILE_PATH), "Requested file does not exist."
    assert FILE_PATH.endswith('fsa'), "Requested file is not a fsa file."

    DATA_FILE = open(FILE_PATH)
    content = DATA_FILE.read()

    assert content != "", "Requested file is empty."
    assert content[0] == ">", "Requested file is not valid fsa file."
except AssertionError as err:
    print("Error:", err.message)
    exit()

stats = Statistic(DATA_FILE)

# time.sleep(5)

statistics = {
    # 'codons_count': stats.count_codons(),
    'nucleotides_count': stats.count_nucleotides(),
}

print(json.dumps(statistics))
