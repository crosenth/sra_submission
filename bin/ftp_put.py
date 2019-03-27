#!/usr/bin/env python
"""
"""
import argparse
import ftplib
import os
import sys


def main(arguments):
    class CustomFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter):
            pass
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument('address')
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('account_folder')
    parser.add_argument('target_folder', help='unique meaningful name')
    parser.add_argument('datadir')
    args = parser.parse_args(arguments)
    session = ftplib.FTP(args.address, args.username, args.password)
    session.cwd(args.account_folder)
    session.mkd(args.target_folder)
    session.cwd(args.target_folder)
    for f in os.listdir(args.datadir):
        pth = os.path.join(args.datadir, f)
        if os.path.islink(pth):
            pth = os.readlink(pth)
        with open(pth, 'rb') as fi:
            print(f)
            session.storbinary('STOR ' + f, fi)
    session.quit()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
