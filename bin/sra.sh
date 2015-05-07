#!/bin/bash

# Upload all fastq files in folder to ncbi

# See http://www.ncbi.nlm.nih.gov/Traces/sra_sub/sub.cgi?login=pda for SRA submission details
# See Dropbox/papers/miseq_v_ion/SRA\ upload/sra_upload_tracker.tsv for details on files

# -c option skips files that are already present on server
# (username,password) -u sra,VfOiVJn1

set -e
set -x

FILES=$(echo *.fastq*)

lftp -e "mput -c ${FILES} ;bye" ftp-private.ncbi.nih.gov -u sra,VfOiVJn1
