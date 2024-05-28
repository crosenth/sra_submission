===============
SRA submissions
===============

.. contents:: Table of Contents

authors
=======

* Noah Hoffman (ngh2@uw.edu)
* Chris Rosenthal (crosenth@uw.edu)

package dependencies
====================

* biopython
* bioscons
* csvkit

Introduction
============

Official walkthrough: http://www.ncbi.nlm.nih.gov/books/NBK47529/

Main submission page: https://submit.ncbi.nlm.nih.gov/

There are three parts to submitting and experiment: the Bioproject, 
the Biosamples and the SRA fastq sequence submissions.

To start, you will need to use a 3rd party login to sign into the std_crc 
NCBI account:

https://ncbiinsights.ncbi.nlm.nih.gov/my-ncbi-login-transition-tips/

After you have set up a 3rd party login it will need to be linked to the 
std_crc NCBI account.  Email the std_crc account administrator to add your
login to the account.

*NOTE*:

At any point during the submission process if there are any issues the SRA staff
is good at answering questions. Just send an email to sra@ncbi.nlm.nih.gov 
to have someone assigned to help through the process.

Data
====

A submission requires access to the datafiles (can be zipped) along with
at least two identifying columns of annotation.  For this example the two
unique, identifying colums are specimen and manuscript_id::

  specimen | manuscript_id
  ------------------------
  p7z1tr10 | S1
  p7z2tr10 | S2
  p7z2tr12 | S3
  ...

Using the specimen name you can deduce the filenames will look something like 
if they were pyrosequenced::

  p7z1tr10.fastq.bz2
  p7z2tr10.fastq.bz2
  p7z2tr12.fastq.bz2

Or have two paired-end sequence files from the Illumina Miseq there will be two
fastq files.  In this example the unique, identifying columns are specimen and
label::

  specimen     | label
  ------------------------
  m47n701-s502 | 901-2
  m47n701-s505 | 901-4
  m47n701-s507 | 901-6
  ...

  m47n701-s502_S1_L001_R1_001.fastq.gz, m47n701-s502_S1_L001_R2_001.fastq.gz
  m47n701-s505_S1_L001_R1_001.fastq.gz, m47n701-s505_S1_L001_R2_001.fastq.gz
  m47n701-s507_S1_L001_R1_001.fastq.gz, m47n701-s507_S1_L001_R2_001.fastq.gz
  ...

All fastq data files are located in the run folders found here::

  /fh/fast/fredricks_d/bvdiversity/data

We have developed scripts to grab these fastq files so you do not
need to go hunting.

Now we are ready to begin the three submission walkthroughs.

Bioproject
==========

https://submit.ncbi.nlm.nih.gov/subs/bioproject/

You can start with the either the Bioproject or Biosample submission 
walkthroughs but the best place to start is with the Bioproject.  The 
Bioproject is considered the "umbrella" point for the Biosamples. Click on 
'New submission' and follow the walkthrough.  The process is fairly 
straight forward.  For example annotations from previous sumbmissions here are
two examples one pyrosequencing and one miseq::

  https://www.ncbi.nlm.nih.gov/bioproject/PRJNA420364
  https://www.ncbi.nlm.nih.gov/bioproject/PRJNA529191

There will be a step that asks for the Biosample accessions.  You will not
have the Biosample accessions at this point and there will be too many
to submit at this point anyway.  Just continue on with the Bioproject
submission process skipping this step. After finishing the walkthrough
a Bioproject accession will be assigned.  Make note of the Bioproject 
accession and continue one to the Biosample submission process.

NOTE: If you have any questions or need to changes just email
sra@ncbi.nlm.nih.gov or bioproject@ncbi.nlm.nih.gov.

Biosample
=========

https://submit.ncbi.nlm.nih.gov/subs/biosample/

Create a 'New submission' Biosample and follow the walkthrough. You will be
asked to submit a tab-delimited file with the sample names filled out and
other required informatiom.  There is a pre-filled template file located in
the template folder that can be used::

  /fh/fast/fredricks_d/bvdiversity/sra/template/MIMS.me.human-vaginal.5.0.tsv

Using this file the following script will automatically put everything
together::

  bin/biosample.py --outdir output/CID_NGU_NCBI_SEQ_Submission_FINAL --max-rows 1000 data/CID_NGU_NCBI_SEQ_Submission_FINAL.tsv sample_name,study_id templates/MIMARKS.survey.human-associated.5.0.tsv PRJNA637612

sample_name must be in form mXXnXXXsXXX

For an explanation script options::

  bin/biosample.py --help

NOTE: NCBI is enforcing a 1,000 row Biosample batch limit.  If you are 
attempting more than 1,000 samples they will be split into multiple
files for multimple Biosample submissions.

Output will look something like this::

  sample_name     | sample_title | bioproject_accession | organism                 | host         | collection_date | geo_loc_name       | lat_lon       | ref_biomaterial | rel_to_oxygen | samp_collect_device | samp_mat_process | samp_size | source_material_id | description | label
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  m47n701-s502    |              | PRJNA529191          | human vaginal metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | 901-2
  m47n701-s505    |              | PRJNA529191          | human vaginal metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | 901-4
  m47n701-s507    |              | PRJNA529191          | human vaginal metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | 901-6
  ...

Upload the table as part of the biosample submission process.  After some time
accession numbers for each sample_name will be generated.  When they are ready
there will be an attributes file for you to download via the main biosample 
submission portal page.  We will use this attributes file to fill out the
final sra sequence upload template.

NOTE: From time to time NCBI will update the MIMARKS.survey.human-vaginal template
which will force us to update our own.  To get the latest template go to::

  https://submit.ncbi.nlm.nih.gov/biosample/template/

Under "GSC MIxS packages for genomes, metagenomes, and marker sequences" 
select "MIMARKS Survey related" -> "human-vaginal" -> "Download TSV".  
Place the tsv file into the templates folder adding any additional required 
annotation and update this README accordingly.

Sequence Upload
===============

https://submit.ncbi.nlm.nih.gov/subs/sra/

This is the last step in the process.  Click on the 'New submission' tab above
and follow the steps.  There will be an sra submission form to fill out and 
submit.  Here is where we upload the fastq data files.  Using your Bioproject 
accession (or if you submitted the Bioproject first it will already be included in
your biosample_accession attributes file) run the `bin/sra_meta.p`  script. Note, 
the same upload limit of 1,000 samples applies here so you may need to go through 
multiple SRA submissions wizards to finish the submission::

  bin/sra_meta.py --outdir output/Overbaugh_NCBISRA/fastq --out output/Overbaugh_NCBISRA/SRA_metadata_acc.tsv data/Overbaugh_NCBISRA.tsv output/Overbaugh_NCBISRA/attributes.tsv templates/SRA_metadata_acc.tsv ../data

Or if a miseq sample then use this script::

  bin/sra_meta_miseq.py --outdir output/LancetHIV_Kelleretal_2019/fastq --out output/LancetHIV_Kelleretal_2019/SRA_metadata_acc.tsv output/LancetHIV_Kelleretal_2019/attributes.tsv templates/SRA_metadata_acc_miseq.tsv ../data

The fastq files will be gathered and placed in the --outdir folder while the
filled out SRA form will placed in --out.  The form file will have one row
per specimen/sample which will look somewhat like this::

  biosample_accession  | title | library_ID | design_description                                                                                                                                                                                                                                                                                    | library_strategy | library_source | library_selection | library_layout | platform | instrument_model    | filetype | filename1 
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  SAMN04859440         | S1    | p7z1tr10   | DNA was extracted using the Bacteremia Kit (Mobio). The V3-V4 region of the 16S rRNA gene was targeted for broad-range PCR with pyrosequencing. 6-bp barcodes were used with the reverse primer to facilitate multiplexing. Reactions were purified using Agencourt AMPure beads prior to sequencing. | AMPLICON         | METAGENOMIC    | PCR               | single         | _LS454   | 454 GS FLX Titanium | fastq    | p7z1tr10.fastq.bz2
  ...

Go ahead and upload the filled out form SRA `--out` file when asked for it.

The last step in this process will have the ftp upload instructions.
They will provide an ftp username, password and upload location.  You will also
need to create a folder to upload the files to. Use the following script with 
the parameters provided from NCBI as follows:

  bin/ftp_put.py ftp-private.ncbi.nlm.nih.gov subftp w4pYB9VQ uploads/ngh2@uw.edu_u25A5oa4 LancetHIV_Kelleretal_2019 output/LancetHIV_Kelleretal_2019/fastq

The username, password and upload folder will change periodically so make sure
to use the latest, correct parameter information.

Gather accessions
=====================
After everything has processed accession data can be acquired by going to the 
SRA Run Selector::

  https://trace.ncbi.nlm.nih.gov/Traces/study/

Enter the Bioproject accession to retrieve the accessions.  Copy and paste the 
Run, Biosample and Experiment accession columns to the original data sheet.

Congratulations, you have completed the sra submission process!
