#!/usr/bin/env python3
"""
Aggregate miseq specimens from multiple projects
"""
import argparse
import os
import pandas
import pathlib
import re
import sys


def main(arguments):
    class CustomFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter):
            pass
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument('biosample_attributes',
                        help=('tab delimited "attributes file" from sra, '
                              'columns [accession,sample_name]'))
    parser.add_argument('template',
                        help=('sra template file with one row '
                              'filled with common column data'))
    parser.add_argument('datadir', help=('base location of plate data'))

    outopts = parser.add_argument_group('output options',)
    outopts.add_argument('--outdir',
                         help=('for individual fastq files'))
    outopts.add_argument('--out', default=sys.stdout,
                         help=('output for sra submission '
                               'tab delimited form'))
    args = parser.parse_args(arguments)
    try:
        os.makedirs(args.outdir)
    except OSError:
        pass
    except TypeError:
        pass
    attributes = pandas.read_csv(
        args.biosample_attributes,
        usecols=['accession', 'sample_name'],
        sep='\t',
        dtype=str)
    template = pandas.read_csv(args.template, sep='\t', dtype=str)
    template = pandas.concat([template] * len(attributes))
    template = template.reset_index(drop=True)
    cols = ['biosample_accession', 'library_ID']
    template[cols] = attributes
    if args.outdir:
        plate_pattern = re.compile(r'^m(?P<plate>\d+)n')
        plates = set()
        for i in template['library_ID'].values:
            plates.add(re.search(plate_pattern, i).group('plate'))
        plate_dirs = re.compile(
            r'miseq-plate-(?:' + '|'.join(plates) + r')$')
        # single walk: index all fastq files keyed by library_ID
        fastq_index = {}
        libraries = set(template['library_ID'].values)
        expected = len(libraries) * 2
        found = 0
        print(f'searching for {expected} fastq files...', file=sys.stderr)
        for plate_dir in os.scandir(args.datadir):
            if not plate_dir.is_dir() or not plate_dirs.match(plate_dir.name):
                continue
            run_files = os.path.join(plate_dir.path, 'run-files')
            if not os.path.isdir(run_files):
                continue
            for root, dirs, files in os.walk(run_files):
                for f in files:
                    if not (f.endswith('_001.fastq.gz')
                            and re.search(r'_R[12]', f)):
                        continue
                    library = f.split('_')[0]
                    if library in libraries:
                        found += 1
                        print(f'\rfound {found}/{expected}',
                              end='', file=sys.stderr)
                        fastq_index.setdefault(library, []).append(
                            os.path.join(root, f))
        print(f'\nfound {found} of {expected} fastq files', file=sys.stderr)
        for i in template['library_ID'].values:
            try:
                r1, r2 = sorted(fastq_index[i])
            except KeyError:
                raise FileNotFoundError(f'no fastq files found for {i}')
            except ValueError as e:
                print('error processing: ' + i)
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
