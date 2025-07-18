#!/usr/bin/env python3
"""Fill out a biosample file given specimen data and a biosample template
"""
import argparse
import glob
import os
import pandas
import re
import sys


def check_sample_name(s):
    if not s.startswith('m'):
        raise ValueError(
                f'invalid sample_name: "{s}". '
                'Are you declaring the right sample_name column?')


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
    parser.add_argument('--previous',
        help='output biosamples that have already been submitted')
    parser.add_argument(
        '--max-rows',
        type=int,
        help=('Cap the number of rows in output. '
              'Currently there is an 1000 row ncbi limit'))
    parser.add_argument('--outdir', default=sys.stdout)
    args = parser.parse_args(arguments)
    try:
        os.makedirs(args.outdir)
    except OSError:
        pass
    if args.previous:
        try:
            prev = os.path.dirname(args.previous)
            os.makedirs(prev)
        except OSError:
            pass
    identifiers = args.identifiers.split(',')
    datecols = []
    if 'collection_date' in identifiers:
        datecols.append('collection_date')
    samples = pandas.read_csv(
        args.samples,
        dtype=str,
        parse_dates=datecols,
        usecols=identifiers,
        sep='\t').dropna()
    samples = samples.rename(
        columns={
            identifiers[0]: '*sample_name',
            'collection_date': '*collection_date'})
    samples['*sample_name'].apply(check_sample_name)
    template = pandas.read_csv(args.template, dtype=str, sep='\t', comment='#')
    template['bioproject_accession'] = args.bioproject
    filled = pandas.concat([template] * len(samples))
    filled = filled.reset_index(drop=True)
    filled[samples.columns] = samples
    if len(identifiers) == 1:
        # use plate, zone and primer if only sample name identifier is given
        def plate_zone_primer(s):
            plate_zone_primer = re.findall(
                '[A-Za-z]+[0-9]+', s['*sample_name'])
            if len(plate_zone_primer) == 2:
                plate_zone_primer.insert(1, '')
            s['plate'], s['zone'], s['primer'] = plate_zone_primer
            return s
        filled = filled.apply(plate_zone_primer, axis=1)
    name, ext = os.path.splitext(os.path.basename(args.template))

    # cross reference with samples already submitted and check if annotations
    # need to be updated from previous submission
    submitted = []
    for fl in glob.iglob(os.path.join('output/**/attributes*.tsv')):
        attr = pandas.read_csv(fl, sep='\t', dtype=str)
        attr = attr[attr['sample_name'].isin(filled['*sample_name'])]
        if not attr.empty:
            dname = os.path.dirname(fl)
            fls = [f for f in os.listdir(dname) if f.startswith('metadata-')]
            if not fls:
                raise FileNotFoundError('missing meta data in dir ' + dname)
            fls = [os.path.join(dname, f) for f in fls]
            for f in fls:
                # may be more than one metadata if sub had > 1000 samples
                submitted.append(pandas.read_csv(f, sep='\t', dtype=str))
    submitted = pandas.concat(submitted)
    submitted = submitted[submitted['library_ID'].isin(filled['*sample_name'])]
    if not submitted.empty:
        if args.previous:
            print('WARNING: Some biosamples were already submitted: ' + args.previous)
            filled = filled[~filled['*sample_name'].isin(submitted['library_ID'])]
            submitted.to_csv(args.previous, index=False, sep='\t')
        else:
            print(submitted)
            raise ValueError('samples already submitted')

    if args.max_rows:
        for i, r in enumerate(range(0, len(filled), args.max_rows), start=1):
            out = os.path.join(args.outdir, name + '_' + str(i) + ext)
            filled[r:r+args.max_rows].to_csv(
                out,
                date_format='%Y-%m-%d',  # collection_date
                index=False,
                sep='\t')
    else:
        out = os.path.join(args.outdir, name + ext)
        filled.to_csv(out, index=False, sep='\t')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
