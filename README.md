Python EUtils
=============

python-eutils is a Client-side Python implementation for the public API of the NCBI Entrez System, 
which allows access to several genomics databases.
Basically, it allows the use of server-side Entrez Programming Utilities (E-utilities)
on https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ via HTTPS requests.

This package has been developed mainly for didactical purposes, during and after a mutual cooperation 
between Biotechnologists and Software Developers in 2018, in part to show the potential of Python 
as a programming language and also to learn how the NCBI Services works.
The initial purpose was to speed-up and make, hopefully, a little bit clearer 
the interrogation process of NCBI's Entrez dbs, in a programmatic way.

While the implementation is far from complete, it has been thorougly documented, focusing on
the ESearch, ELink, EFetch and EPost operations, and pointing to the proper help pages 
on NCBI website where necessary.

Official Documentation and Sample Applicatons have of course been followed to make this implementation possible,
as well as the original Perl scripts, available on https://www.ncbi.nlm.nih.gov/books/NBK25498/ .

Getting Started:
================

Simply clone this repository:

        git clone https://gitlab.com/bio.info/NCBI/python-eutils.git


Setup developement environment:
===============================

Install package requirements as a superuser by issuing:

        # pip3 install -r requirements.txt

or as a regular user:

        $ pip3 install --user -r requirements.txt

And make your changes to the source code.

Install as a Python package:
===========================

Package setup is offered via setup.py and is not available on PyPi at the time of writing.
Simply install it as superuser by issuing:

        # python3.8 setup.py install

Or as a user package:

        $ pip3 install --user .


Documentation:
==============

For a proper documentation, follow the python inline help command:

        >> import python_eutils as pyeu
        >> help(pyeu)

Or refer to ``The E-Utilities in-Depth'' on https://www.ncbi.nlm.nih.gov/books/NBK25499/ .

Features:
=========

Python EUtils comes with some extra features like Operations Pipelining which allows to easily perform complex
operations in a small amount of code.

For a deeper look into how code has been simplified, have a look to the original Perl scripts
under ``Advanced Pipelining'' section at:

https://www.ncbi.nlm.nih.gov/books/NBK25497/?report=classic#_chapter2_Combining_Eutility_Calls_to_Cre_


        [...]
        Retrieving data records in database B linked to records in database A matching an Entrez query

        ESearch → ELink → ESummary

        ESearch → ELink → EFetch
        [...]

and to the corresponding test cases in this tree under test/
        
        tests/
        ├── __init__.py
        ├── pubmed_protein_esummary.py
        └── pubmed_protein_fetch.py


The following image shows how to programmatically implement a ESearch-ELink-EFetch pipeline:

![ESearch-Elink-EFetch pipeline] (https://gitlab.com/bio.info/NCBI/python-eutils/-/blob/master/docs/Pipelines.png)

Further testcases and bugfixes may come in the future (as well as new features and a proper documentation).
Of course, feedbacks and suggestions are always appreciated :)

N.B. 

Since NCBI API Keys are not yet supported in this implementation (only HTTPS GET or POST),
a rate-limiter of 1-second between requests has been introduced. 
Use with care and do not overburden the NCBI servers with too much requests. 
The creator does not hold any responsibility in the misuse of this software.

Also carefully read COPYRIGHT.NLM, for any use of downloaded data from NCBI System, 
publication and redistribution included.

For a complete NLM copyright policy have a look at https://www.nlm.nih.gov/copyright.html






