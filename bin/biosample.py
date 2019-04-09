#!/usr/bin/env python

"""Fill out a biosample file given specimen data and a biosample template
"""

import argparse
import pandas
import re
import sys


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'samples', help='tab seperated file with column specimen')
    parser.add_argument(
        'identifiers',
        help=('the sample name column and, optionally, any more '
              'identifying column names coma delimited. If just '
              'the sample column specified then the script will '
              'attempt to parse the plate, zone and primer from '
              'the sample name.'))
    parser.add_argument(
        'template',
        help=('biosample template file with one row '
              'filled out with required columns'))
    parser.add_argument('bioproject', help='bioproject accession')
    parser.add_argument('--out', default=sys.stdout)
    args = parser.parse_args(arguments)
    identifiers = args.identifiers.split(',')
    samples = pandas.read_csv(
        args.samples,
        dtype=str,
        usecols=identifiers,
        sep='\t').dropna()
    samples = samples.rename(columns={identifiers[0]: '*sample_name'})
    template = pandas.read_csv(args.template, dtype=str, sep='\t')
    template['bioproject_accession'] = args.bioproject
    filled = pandas.concat([template] * len(samples))
    filled = filled.reset_index(drop=True)
    filled[samples.columns] = samples
    if len(identifiers) == 1:
        # use plate, zone and primer if only sample name identifier is given
        def plate_zone_primer(series):
            plate_zone_primer = re.findall('\D+\d+', series['*sample_name'])
            if len(plate_zone_primer) == 2:
                plate_zone_primer.insert(1, '')
            series['plate'], series['zone'], series['primer'] = plate_zone_primer
            return series
        filled = filled.apply(plate_zone_primer, axis=1)
    filled.to_csv(args.out, index=False, sep='\t')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
