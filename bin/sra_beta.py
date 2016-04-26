#!/usr/bin/env python

"""Aggregate specimens from multiple projects

"""

import bz2
import os
import pandas
import sys
import argparse
import re
import glob

from Bio import SeqIO

LABELS_HEADER = ['specimen', 'filename', 'md5sum']


class Multifile(object):
    def __init__(self, dirname, compressed=True):
        assert os.path.exists(dirname)
        self.dirname = dirname
        self.files = {}
        self.compressed = compressed

    def __getitem__(self, key):
        if key in self.files:
            fn, fobj = self.files[key]
        elif self.compressed:
            fn = os.path.join(self.dirname, '{}.fastq.bz2'.format(key))
            fobj = bz2.BZ2File(fn, 'w')
            self.files[key] = (fn, fobj)
        else:
            fn = os.path.join(self.dirname, '{}.fastq'.format(key))
            fobj = open(fn, 'w')
            self.files[key] = (fn, fobj)

        return fobj

    def filename(self, key):
        return os.path.basename(self.files[key][0])

    def items(self):
        return self.files.items()

    def close(self):
        for fn, fobj in self.files.values():
            fobj.close()


def get_fastqs(datadir, keep):
    """Read .fna and .qual files in `datadir` and return an iterator of
    sequence records.

    """

    assert isinstance(keep, dict)

    fnafiles = sorted(glob.glob(os.path.join(datadir, '?.TCA.454Reads.fna')))
    qualfiles = sorted(glob.glob(os.path.join(datadir, '?.TCA.454Reads.qual')))

    assert fnafiles
    assert len(fnafiles) == len(qualfiles)

    for fna, qual in zip(fnafiles, qualfiles):
        with open(fna) as f, open(qual) as q:
            records = SeqIO.QualityIO.PairedFastaQualIterator(f, q)
            for rec in records:
                if rec.id in keep:
                    yield rec, keep[rec.id]


def main(arguments):
    class CustomFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter):
            pass

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=CustomFormatter)

    parser.add_argument('specimens',
                        help=('tab delimited with columns '
                              '[specimen,biosample_accession]'))
    parser.add_argument('bioproject_accession',
                        help=('bioproject accession number'))
    parser.add_argument('template',
                        help=('sra template file with one row '
                              'filled with common column data'))
    parser.add_argument('--datadir',
                        default='/fh/fast/fredricks_d/bvdiversity/data',
                        help=('top level data directory'))

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
        usecols=['specimen', 'manuscript_id', 'biosample_accession'],
        sep='\t')

    template = pandas.read_csv(args.template, sep='\t')
    template = pandas.concat([template] * len(specimens))
    template = template.reset_index(drop=True)
    template[['title', 'library_ID', 'biosample_accession']] = specimens
    template['bioproject_accession'] = args.bioproject_accession

    pattern = args.datadir + '/(plate|junior-plate)-\d+/quality-filter$'

    fqfiles = Multifile(args.outdir, compressed=True)

    for dirpath, _, _ in os.walk(args.datadir):
        if re.search(pattern, dirpath):
            seqnames = pandas.read_csv(
                os.path.join(dirpath, 'combined.map.csv'),
                header=None,
                squeeze=True,
                names=['seqname', 'specimen'],
                usecols=['seqname', 'specimen'],
                index_col='seqname')
            seqnames = seqnames[seqnames.isin(specimens['specimen'])]

            print(dirpath + ' ' + str(len(seqnames)))

            if seqnames.empty:
                continue

            # write fastqs
            raw_data = os.path.join(os.path.dirname(dirpath), 'raw', 'data')
            fastqs = get_fastqs(raw_data, seqnames.to_dict())
            for rec, specimen in fastqs:
                SeqIO.write([rec], fqfiles[specimen], 'fastq')

    fqfiles.close()

    # record fastq filenames
    template['filename1'] = template['library_ID'].apply(
        lambda x: fqfiles.filename(x))

    template.to_csv(args.out, index=False, sep='\t')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
