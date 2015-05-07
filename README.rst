===============
SRA submissions
===============

.. contents:: Table of Contents

authors
=======

* Chris Rosenthal

package dependencies
====================

* biopython
* bioscons
* csvkit

Introduction
============

Submission to the SRA is an evolving process on there end (and ours). Some 
of that process has been automated here but much of it requires manual editing,
copying and pasting.

A link to the main submission page is here: https://submit.ncbi.nlm.nih.gov/

There are three parts to submitting and experiment: a biosample, a bioproject 
and the sequence submission.

For examples of all three pars see Sujatha Srinivasan's Vaginal Bacteria
project::

  username: std_crc
  password: Gram$positive4

They are pretty good at answering questions and making corrections on their
end.  Just send an email to sra@ncbi.nlm.nih.gov to have someone assigned to
help through the process.

Data
====

A submission requires access to the datafiles (in some zip format) along with
at least two lines of annotation: specimen names and manuscript ids:: 

  specimen | manuscript_id
  ------------------------
  p7z1tr10 | S1
  p7z2tr10 | S2
  p7z2tr12 | S3

In this example the fileanames are::

  p7z1tr10.fastq
  p7z2tr10.fastq
  p7z2tr12.fastq

Biosample
=========

https://submit.ncbi.nlm.nih.gov/subs/biosample/

Create a new Biosample and follow the walkthrough. You will also need to
complete a template to upload.  In Sujatha's metagenome environment example the specimen
column becomes sample_name and manuscript_id becomes source_material_id::

  sample_name | description | bioproject_id | sample_title  | organism host    | isolation_source | collection_date | geo_loc_name       | lat_lon       | ref_biomaterial | rel_to_oxygen | samp_collect_device | samp_mat_process | samp_size | source_material_id
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  p7z1tr10    |             |               |               | human metagenome |  Homo sapiens    | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           | S1
  p7z2tr10    |             |               |               | human metagenome |  Homo sapiens    | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           | S2
  p7z2tr12    |             |               |               | human metagenome |  Homo sapiens    | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           | S3

Upload the table to finish the Biosample.  Accession numbers for each sample_name will be
generated and we will use those numbers for the eventual sequence upload step.

Bioproject
==========

https://submit.ncbi.nlm.nih.gov/subs/bioproject/

Follow the steps and walkthrough to create the bioproject. There should be no
information to upload at this point.  If there is a single sample/specimen 
for the project then you can enter it in here.

Sequence Upload
===============

This is the step that ties everything together. There are essentially three
steps within this step to complete the SRA submission.  First we will need
to zip up the sequences if we have not yet::

  bzip2 p7z1tr10.fastq p7z2tr10.fastq p7z2tr12.fastq

Which gives us::

  p7z1tr10.fastq.bz2
  p7z2tr10.fastq.bz2
  p7z2tr12.fastq.bz2

At this point we can generate our md5check sums as well::

  md5sum p7z1tr10.fastq.bz2 p7z2tr10.fastq.bz2 p7z2tr12.fastq.bz2

Which gives us something like this::

  ae6f3d5bba6833c199fdc6ef7fffab36  p7z1tr10.fastq.bz2
  89e033040e133f397c508a26f5ce1624  p7z2tr10.fastq.bz2
  f4e1bba12dc8090dbb4b6891735cec97  p7z2tr12.fastq.bz2

The md5 sums are a way to ensure that the actual files were successfully 
uploaded.  The SRA people will generate the same numbers on their end to 
compare and confirm that the files were not corrupted during upload.

The next step is to fill out the data/SRA_subtemplate_v2-7-chris.xlsx.  For an
example of how to fill this out see the notes/ folder. You will need the
sample_name(s) and manuscript_id(s), as well as the bioproject accession number
and biosample accession numbers, filenames and md5 sums generated earlier.  
Once you have filled that out send the excel sheet to sra@ncbi.nlm.nih.gov.
They will assign you a person to help finish the submission and make any 
corrections.

Automation
==========

See the Sconstruct file to see a little bit of automation.  The script
bin/walk_data.py creates the fastq files and generates the md5 sums. 
Again, this information was later hand copied into the 
data/SRA_subtemplate_v2-7-chris.xlsx spreadsheet.
