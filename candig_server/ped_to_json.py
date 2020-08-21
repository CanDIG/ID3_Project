#!/usr/bin/env python3
"""
convert ancestry information into a minimal candig-ingest JSON file
"""
import argparse
import csv
import json

def ingest_dicts_from_ped(pedfile):
    patintlist = []
    pedreader = csv.DictReader(pedfile, delimiter='\t')
    for row in pedreader
Family ID	Individual ID	Paternal ID	Maternal ID	Gender	Phenotype	Population	Relationship	Siblings	Second Order	Third Order	Children	Other Comments

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_ped', help='path to the input .ped file; stdin if not provided',
            type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    
    

if __name__ == "__main__":
    main()
