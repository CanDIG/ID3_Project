#!/usr/bin/env python3
"""
convert ancestry information into a minimal candig-ingest JSON file
"""
import argparse
import csv
import json
import sys

def dicts_from_ped(pedfile):
    patientlist = []
    pedreader = csv.DictReader(pedfile, delimiter='\t')
    for row in pedreader:
        patid = row["Individual ID"]
        ethnicity = row["Population"]
        patient = { "Patient": { "patientId": patid, "ethnicity": ethnicity },
                    "Sample": { "patientId": patid, "sampleId": f"SAMPLE_{patid}" } }
        patientlist.append(patient)
    return patientlist

def patientlist_to_json(patient_list):
    metadata = {"metadata": patient_list}
    return json.dumps(metadata)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_ped', help='path to the input .ped file',
            type=argparse.FileType('r'))
    parser.add_argument('output_json', help='path to the output json file, stdout if not provided',
            type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    
    patient_list = dicts_from_ped(args.input_ped)
    print(patientlist_to_json(patient_list), file=args.output_json)
    
if __name__ == "__main__":
    main()
