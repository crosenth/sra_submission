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

Official walkthrough: http://www.ncbi.nlm.nih.gov/books/NBK47529/

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
at least two lines of annotation: specimen names and manuscript ids.  

For example:: 

  specimen | manuscript_id
  ------------------------
  p7z1tr10 | S1
  p7z2tr10 | S2
  p7z2tr12 | S3

And in this example the fileanames are::

  p7z1tr10.fastq.bz2
  p7z2tr10.fastq.bz2
  p7z2tr12.fastq.bz2

The file may have a number of different column names.  The only columns that matter
are specimen and manuscript_id which may need to be renamed to specimen and
manuscript_id.  The file may need to be converted from an xlsx file to a tab 
delimited file.  The sra submission process requires tab delimited files for 
upload so that is our default file format for this process.

Biosample
=========

https://submit.ncbi.nlm.nih.gov/subs/biosample/

Create a 'New submission' Biosample and follow the walkthrough. The is a 
Metagenome-environment.tsv template file you will need to fill out for this
step of the submission.  You can download a template from the ncbi biosample 
submission page or use the one in the templates folder 
templates/Metagenome.environmental.1.0.tsv.  Finally, you can run this script
need to complete a template to upload::

  bin/biosample.py --out output/msflash_ncbisra_final/MIMS.me.human-vaginal.4.0.tsv data/msflash_ncbisra_final.tsv templates/MIMS.me.human-vaginal.4.0.tsv

Output will look like this::

  sample_name | sample_title | bioproject_accession | organism         | host         | collection_date | geo_loc_name       | lat_lon       | ref_biomaterial | rel_to_oxygen | samp_collect_device | samp_mat_process | samp_size | source_material_id | description | plate | zone | primer
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  p7z1tr10    |              |                      | human metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | p7    | z1   | tr10
  p7z2tr10    |              |                      | human metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | p7    | z2   | tr10
  p7z2tr12    |              |                      | human metagenome | Homo sapiens | missing         | "USA: Seattle, WA" | not collected |                 |               |                     |                  |           |                    |             | p7    | z2   | tr12

The bioproject_accession will be blank as we have not yet created a Bioproject.
Upload the table as part of the biosample submission process.  After some time
accession numbers for each sample_name will be generated. We will use those numbers 
for the sequence upload step.

There is just one manual data entry process at this point.  You will need to 
add a biosample_accession column to the original data sheet
(for example data/Gorgos_Sycuro_SDC_Table_S1.tsv). The original data sheet will look something 
like this::

  specimen | manuscript_id | biosample_accession
  ----------------------------------------------
  p7z1tr10 | S1            | SAMN03581187
  p7z2tr10 | S2            | SAMN03581188
  p7z2tr12 | S3            | SAMN03581189

This is necessary for the Sequence Upload step later on as well as for 
reporting back to Sujatha what her various accession numbers are.

Bioproject
==========

https://submit.ncbi.nlm.nih.gov/subs/bioproject/

After you receive your biosample accessions got the bioproject submission page
and follow the walkthrough to create the bioproject. There is no information to 
upload at this point, just the walkthrough.  You will also enter your biosample 
accessions here.  After you have submitted 

Note: After this step you can update the bioproject_accession column in the
biosample by sending an email to biosamplehelp@ncbi.nlm.nih.gov and telling
them what the bioproject is for which biosample.

Sequence Upload
===============

https://submit.ncbi.nlm.nih.gov/subs/sra/

This is the last step in the process.  Click on the 'New submission' tab above
and follow the steps.  There will be an sra submission form to fill
out and submit.  There will also be fastq files to upload.  Using your bioproject 
accession (or if you submitted the Bioproject first it will already be included in
your biosample_accession attributes file) and filled in biosample_accession column 
in the original data sheet run the following script::

  bin/sra_meta.py --outdir output/msflash_ncbisra_final/fastq --out output/msflash_ncbisra_final/SRA_metadata_acc.tsv data/msflash_ncbisra_final.tsv output/msflash_ncbisra_final/attributes.tsv templates/SRA_metadata_acc.tsv

Which will generate a prefilled form to upload as well as upload the fastq 
files and output them in the --outdir directory.  The generated form --out will 
look something like this::

  biosample_accession  | bioproject_accession | title | library_ID | design_description                                                                                                                                                                                                                                                                                    | library_strategy | library_source | library_selection | library_layout | platform | instrument_model    | filetype | filename1 
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  SAMN04859440         | PRJNA319051          | S1    | p7z1tr10   | DNA was extracted using the Bacteremia Kit (Mobio). The V3-V4 region of the 16S rRNA gene was targeted for broad-range PCR with pyrosequencing. 6-bp barcodes were used with the reverse primer to facilitate multiplexing. Reactions were purified using Agencourt AMPure beads prior to sequencing. | AMPLICON         | METAGENOMIC    | PCR               | single         | _LS454   | 454 GS FLX Titanium | fastq    | p7z1tr10.fastq.bz2

Go ahead and upload that form --out file where it asks for it.

Lastly, use of the uplooad options specified on the 
https://submit.ncbi.nlm.nih.gov/subs/sra/ page.  The options change often so
I will not go into to much specificity on what approach works best.  I chose
the Aspera command line option and followed the directions to upload the files
in the fastq directory.

Finally
=======
When you get the specimen accessions create another column called 
'sequence_accession' in the data sheet (data/Gorgos_Sycuro_SDC_Table_S1.tsv) 
and manually enter the sequence accessions.  Write an email to Sujatha
giving the project accession, study accession 

(go to https://www.ncbi.nlm.nih.gov/Traces/sra_sub/sub.cgi and find the SRP
number near the bioproject accession number)

and a copy of the updated tsv file (data/Gorgos_Sycuro_SDC_Table_S1.tsv) with
the two new accession columns converted **back** to an xlsx.

Congratulations, you have completed the sra submission process!

TODO
====

Create a search database to find biosample accessions from previously submitted
samples to reuse in new bioprojects.
