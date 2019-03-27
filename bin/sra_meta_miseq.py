#!/usr/bin/env python
"""
Aggregate miseq specimens from multiple projects
"""
import os
import pandas
import sys
import argparse
import glob


def main(arguments):
    class CustomFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter):
            pass
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument('bioproject_accession',
                        help=('bioproject accession number if no column '
                              'in --biosample_accessions'))
    parser.add_argument('specimens',
                        help=('tab delimited with columns '
                              '[specimen,manuscript_id]'))
    parser.add_argument('biosample_attributes',
                        help=('tab delimited "attributes file" from sra, '
                              'columns [accession,sample_name]'))
    parser.add_argument('template',
                        help=('sra template file with one row '
                              'filled with common column data'))
    parser.add_argument('datadir', help=('base location of plate data'))

    outopts = parser.add_argument_group('output options',)
    outopts.add_argument('--outdir', default='.',
                         help=('for individual fastq files'))
    outopts.add_argument('--out', default=sys.stdout,
                         help=('output for sra submission '
                               'tab delimited form'))
    args = parser.parse_args(arguments)
    try:
        os.makedirs(args.outdir)
    except OSError:
        pass
    specimens = pandas.read_csv(
        args.specimens,
        usecols=['specimen'],
        sep='\t',
        dtype=str)
    attributes = pandas.read_csv(
        args.biosample_attributes,
        usecols=['accession', 'sample_name'],
        sep='\t',
        dtype=str)
    attributes['bioproject_accession'] = args.bioproject_accession
    specimens = specimens.merge(
        attributes, left_on='specimen', right_on='sample_name')
    template = pandas.read_csv(args.template, sep='\t')
    template = pandas.concat([template] * len(specimens))
    template = template.reset_index(drop=True)
    template_cols = [
        'library_ID', 'biosample_accession', 'bioproject_accession']
    specimen_cols = ['specimen', 'accession', 'bioproject_accession']
    template[template_cols] = specimens[specimen_cols]
    pattern = os.path.join(
        args.datadir,
        'miseq-plate-*',
        'run-files',
        '*',
        'Data',
        'Intensities',
        'BaseCalls',
        '{}_*_L001_R[12]*_001.fastq.gz')
    for i in template['library_ID'].values:
        try:
            r1, r2 = sorted(glob.glob(pattern.format(i)))
        except ValueError as e:
            print('error processin:' + i)
            raise(e)
        r1_basename = os.path.basename(r1)
        r2_basename = os.path.basename(r2)
        os.symlink(os.path.abspath(r1), os.path.join(args.outdir, r1_basename))
        os.symlink(os.path.abspath(r2), os.path.join(args.outdir, r2_basename))
        template.loc[template['library_ID'] == i, 'filename'] = r1_basename
        template.loc[template['library_ID'] == i, 'filename2'] = r2_basename
    template.to_csv(args.out, sep='\t', index=False)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
