#!/usr/bin/env python3
"""
Append accession data to original sample_sheet
"""
import argparse
import pandas
import sys


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'sample_sheet', help='original sample sheet in tsv format')
    parser.add_argument(
        'metadata',
        nargs='+',
        help='metadata with accessions associated with study in csv format')
    parser.add_argument('--out', default=sys.stdout)
    args = parser.parse_args(arguments)
    sample_sheet = pandas.read_csv(args.sample_sheet, sep='\t', dtype=str)
    metadata = []
    for m in args.metadata:
        m = pandas.read_csv(m, dtype=str)
        m = m.rename(columns={
            'Run acc': 'accession',
            'Run': 'accession',
            'SRA Study': 'study',
            'SRA study': 'study',
            'BioProject': 'bioproject_accession',
            'Prj acc': 'bioproject_accession',
            'Sample acc': 'biosample_accession',
            'BioSample': 'biosample_accession',
            'Exp acc': 'experiment_accession',
            'Experiment': 'experiment_accession',
            'Library Name': 'library_ID',
            'Library name': 'library_ID',
            })
        m = m[['library_ID', 'accession', 'study', 'bioproject_accession',
               'biosample_accession', 'experiment_accession']]
        metadata.append(m)
    metadata = pandas.concat(metadata)
    sample_sheet = sample_sheet.merge(
        metadata, left_on='seqid', right_on='library_ID')
    sample_sheet.to_csv(args.out, index=False)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
