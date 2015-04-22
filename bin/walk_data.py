#!/usr/bin/env python

"""Aggregate specimens from multiple projects

"""

import bz2
import hashlib
import os
import sys
import argparse
import re
import csv
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
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('specimens',
                        help="file containing specimen ids",
                        type=argparse.FileType('r'))
    parser.add_argument('--seqs', default='seqs.fasta',
                        type=argparse.FileType('w'))
    parser.add_argument('--seq-info', default='seq_info.csv',
                        type=argparse.FileType('w'))
    parser.add_argument('--md5sums', default='md5sums.csv',
                        type=argparse.FileType('w'),
                        metavar='CSV',
                        help=str(LABELS_HEADER))
    parser.add_argument('--fastq-dir', default='output/fastq')

    args = parser.parse_args(arguments)

    try:
        os.makedirs(args.fastq_dir)
    except OSError:
        pass

    specimens = {r['specimen'] for r in csv.DictReader(args.specimens)
                 if r['specimen']}

    info_writer = csv.writer(args.seq_info)

    kept_specimens = set()
    topdir = '/fh/fast/fredricks_d/bvdiversity/data'
    pattern = r'' + topdir + '/(plate|junior-plate)-\d+/quality-filter$'

    fqfiles = Multifile(args.fastq_dir, compressed=True)
    for dirpath, dirnames, filenames in os.walk(topdir):
        if re.search(pattern, dirpath):
            seq_file = os.path.join(dirpath, 'combined.fasta')
            print seq_file
            assert os.path.exists(seq_file)
            info_file = os.path.join(dirpath, 'combined.map.csv')
            assert os.path.exists(info_file)

            with open(seq_file) as seqs, open(info_file) as info:
                keep = [row for row in csv.reader(info) if row[1] in specimens]
                print dirpath, len(keep)
                if len(keep) == 0:
                    continue

                seqnames = {n for n, s in keep}
                kept_specimens |= {s for n, s in keep}
                info_writer.writerows(keep)
                seqs = (s for s in SeqIO.parse(seqs, 'fasta'))
                seqs = (s for s in seqs if s.id in seqnames)
                SeqIO.write(seqs, args.seqs, 'fasta')

            # write fastqs
            raw_data = os.path.join(os.path.dirname(dirpath), 'raw', 'data')
            fastqs = get_fastqs(raw_data, dict(keep))
            for rec, specimen in fastqs:
                SeqIO.write([rec], fqfiles[specimen], 'fastq')

    fqfiles.close()

    # write md5sums of the fastqs
    md5sums = csv.DictWriter(args.md5sums, fieldnames=LABELS_HEADER)
    md5sums.writeheader()
    for specimen, (_, fastq) in fqfiles.items():
        md5sum = hashlib.md5(open(fastq.name).read()).hexdigest()
        filename = os.path.basename(fastq.name)
        md5sums.writerow(dict(specimen=specimen,
                              filename=filename,
                              md5sum=md5sum))

    print 'specimens - kept_specimens', specimens - kept_specimens
    print 'kept_specimens - specimens', kept_specimens - specimens
    assert specimens == kept_specimens

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
