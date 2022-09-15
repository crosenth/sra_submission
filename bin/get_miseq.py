#!/usr/bin/env python3
"""
Gather miseq sequences
"""
import argparse
import os
import pathlib
import re
import sys


def main(arguments):
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                          argparse.RawTextHelpFormatter):
        pass
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument('library_ids', help='headerless txt file')
    parser.add_argument('datadir', help='base location of plate data')
    outopts = parser.add_argument_group('output options')
    outopts.add_argument(
        '--outdir', default='.', help='for individual fastq files')
    args = parser.parse_args(arguments)
    try:
        os.makedirs(args.outdir)
    except OSError:
        pass
    file_pattern = os.path.join(
        args.datadir,
        'miseq-plate-{plate}',
        'run-files',
        '**',
        '{library}_*_L001_R[12]*_001.fastq.gz')
    plate_pattern = re.compile('^m(?P<plate>\d+)n')
    ids = (i.strip() for i in open(args.library_ids))
    for n, i in enumerate(ids):
        plate = re.search(plate_pattern, i).group('plate')
        try:
            pth = pathlib.Path(args.datadir)
            fqs = pth.glob(file_pattern.format(library=i, plate=plate))
            r1, r2 = sorted(fqs)
            r1_basename = os.path.basename(r1)
            r2_basename = os.path.basename(r2)
            print(str(n) + ' ' + r1_basename)
            print(str(n) + ' ' + r2_basename)
            os.symlink(
                os.path.abspath(r1), os.path.join(args.outdir, r1_basename))
            os.symlink(
                os.path.abspath(r2), os.path.join(args.outdir, r2_basename))
        except ValueError as e:
            print('error processing: ' + i)
            raise(e)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
