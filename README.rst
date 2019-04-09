===============
SRA submissions
===============

.. contents:: Table of Contents

authors
=======

* Noah Hoffman
* Chris Rosenthal

package dependencies
====================

* biopython
* bioscons
* csvkit

Introduction
============

Official walkthrough: http://www.ncbi.nlm.nih.gov/books/NBK47529/

Submission to the SRA is an evolving process on there end and ours. Some 
of that process has been automated here but much of it requires manual editing,
copying and pasting.

A link to the main submission page is here: https://submit.ncbi.nlm.nih.gov/

There are three parts to submitting and experiment: a bioproject, a biosample,
and the sequence submission.

To start, here is the login credentials that have been used thus far for
submissions::

  username: std_crc
  password: Gram$positive4

Since BioProject submission PRJNA529191 any NCBI user who is a member of the
'19790-shared-submissions' group should have permissions to view, edit and
make submissions for the Lab.

At any point during the submission process if there are any issues the SRA staff
is pretty good at answering questions. Just send an email to sra@ncbi.nlm.nih.gov 
to have someone assigned to help through the process.

Data
====

A submission requires access to the datafiles (in some zip format) along with
at least two identifying columns of annotation.  For this example we can use
specimen and manuscript_id::

  specimen | manuscript_id
  ------------------------
  p7z1tr10 | S1
  p7z2tr10 | S2
  p7z2tr12 | S3

Using the specimen name you can deduce the filenames will look something like 
if they were pyrosequenced::

  p7z1tr10.fastq.bz2
  p7z2tr10.fastq.bz2
  p7z2tr12.fastq.bz2

Or have two paired-end sequence files from the Illumina Miseq::

  specimen     | label
  ------------------------
  m47n701-s502 | 901-2
  m47n701-s505 | 901-4
  m47n701-s507 | 901-6

  m47n701-s502_S1_L001_R1_001.fastq.gz m47n701-s502_S1_L001_R2_001.fastq.gz
  m47n701-s505_S1_L001_R1_001.fastq.gz m47n701-s505_S1_L001_R2_001.fastq.gz
  m47n701-s507_S1_L001_R1_001.fastq.gz m47n701-s507_S1_L001_R2_001.fastq.gz

All fastq data files are located somewhere in the run folders found in this
directory::

  /fh/fast/fredricks_d/bvdiversity/data

We have developed scripts to grab these fastq files so you do not
need to hunting.

Copy the datafile over the sra data folder::

  /fh/fast/fredricks_d/bvdiversity/sra/data

And make note of the which columns you will use for specimen and the secondary
identifier.  We will use that information to complete the Biosample process.

Bioproject
==========

https://submit.ncbi.nlm.nih.gov/subs/bioproject/

You can start with the either the Bioproject or Biosample submission 
walkthroughs.  Since the Bioproject is considered the "umbrella" point for 
all the Biosamples we will start with the Bioproject.  Just click on 
'New submission' and follow the walkthrough.  The process is fairly 
straight forward.  For example annotations from previous sumbmissions here is 
one pyrosequencing and one miseq example::

  https://www.ncbi.nlm.nih.gov/bioproject/PRJNA420364
  https://www.ncbi.nlm.nih.gov/bioproject/PRJNA529191

There will be a step that asks for the Biosample accessions.  You will not
have the Biosample accessions at this point and there will be too many
to submit at this point anyway.  Just continue on with the Bioproject
submission process skipping this step.  The final step of this README
will be where we tie this all together.

Again, if you have any questions or need to changes just email
sra@ncbi.nlm.nih.gov or bioproject@ncbi.nlm.nih.gov.

Biosample
=========

https://submit.ncbi.nlm.nih.gov/subs/biosample/

Create a 'New submission' Biosample and follow the walkthrough. You will be
asked to submit a tab-delimited file with the sample names filled out with
other required informatiom.  There is a pre-filled template file located in
the template folder that can be used::

  /fh/fast/fredricks_d/bvdiversity/sra/template/MIMS.me.human-vaginal.5.0.tsv

Using this file and the data file you can run this script to put it all 
together::

  bin/biosample.py --bioproject PRJNA529191 --out output/output/LancetHIV_Kelleretal_2019/MIMS.me.human-vaginal.5.0.tsv data/LancetHIV_Kelleretal_2019_table.tsv specimen,label templates/MIMS.me.human-vaginal.5.0.tsv

Output will look something like this::

  sample_name     | sample_title | bioproject_accession | organism                 | host         | collection_date | geo_loc_name       | lat_lon       | ref_biomaterial | rel_to_oxygen | samp_collect_device | samp_mat_process | samp_size | source_material_id | description | label
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  m47n701-s502    |              | PRJNA529191          | human vaginal metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | 901-2
  m47n701-s505    |              | PRJNA529191          | human vaginal metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | 901-4
  m47n701-s507    |              | PRJNA529191          | human vaginal metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | 901-6

Upload the table as part of the biosample submission process.  After some time
accession numbers for each sample_name will be generated.  When they are ready
there will be an attributes file for you to download via the main biosample 
submission portal page.  We will use this attributes file to fill out the
final sra sequence upload template.

NOTE: From time to time NCBI will update the MIMS.me.human-vaginal template
which will force us to update our own.  To get the latest template go to::

  https://submit.ncbi.nlm.nih.gov/biosample/template/

Select "Genome, metagenome or marker sequences (MIxS compliant)" ->
"Environmental/Metagenome Genomic Sequences MIMS" -> "human-vaginal" ->
"Download TSV".  Place the tsv file into the templates folder and update this
README accordingly.

Sequence Upload
===============

https://submit.ncbi.nlm.nih.gov/subs/sra/

This is the last step in the process.  Click on the 'New submission' tab above
and follow the steps.  There will be an sra submission form to fill
out and submit.  There will also be fastq files to upload.  Using your vbioproject 
accession (or if you submitted the Bioproject first it will already be included in
your biosample_accession attributes file) and filled in biosample_accession column 
in the original data sheet run the following script::

  bin/sra_meta.py --outdir output/Overbaugh_NCBISRA/fastq --out output/Overbaugh_NCBISRA/SRA_metadata_acc.tsv data/Overbaugh_NCBISRA.tsv output/Overbaugh_NCBISRA/attributes.tsv templates/SRA_metadata_acc.tsv ../data

If it is a miseq sample then use this script::

  bin/sra_meta_miseq.py output/LancetHIV_Kelleretal_2019/attributes.tsv templates/SRA_metadata_acc_miseq.tsv ../data

The fastq files will be gathered and placed in the --outdir folder while the
filled out SRA form will be output to --out.  The form file will have one row
per specimen/sample which will look somewhat like this::

  biosample_accession  | bioproject_accession | title | library_ID | design_description                                                                                                                                                                                                                                                                                    | library_strategy | library_source | library_selection | library_layout | platform | instrument_model    | filetype | filename1 
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  SAMN04859440         | PRJNA319051          | S1    | p7z1tr10   | DNA was extracted using the Bacteremia Kit (Mobio). The V3-V4 region of the 16S rRNA gene was targeted for broad-range PCR with pyrosequencing. 6-bp barcodes were used with the reverse primer to facilitate multiplexing. Reactions were purified using Agencourt AMPure beads prior to sequencing. | AMPLICON         | METAGENOMIC    | PCR               | single         | _LS454   | 454 GS FLX Titanium | fastq    | p7z1tr10.fastq.bz2

Go ahead and upload that form --out file when asked for it.

Lastly, use the ftp upload options specified on the 
https://submit.ncbi.nlm.nih.gov/subs/sra/ page.  Follow the directions to
upload the fastq files.  I created a helper ftp script which can be used like
this::

  bin/ftp_put.py ftp-private.ncbi.nlm.nih.gov subftp w4pYB9VQ uploads/ngh2@uw.edu_u25A5oa4 LancetHIV_Kelleretal_2019 output/LancetHIV_Kelleretal_2019/fastq

The username and password will change each time you go through this process.

Finally
=======
When you get the specimen accessions create another column called
'sequence_accession' in the data sheet (data/Gorgos_Sycuro_SDC_Table_S1.tsv) 
and manually enter the sequence accessions.  Write an email to Sujatha
giving her the updated data sheet with the specimen accessions and also she
will need the project accession 

Congratulations, you have completed the sra submission process!
