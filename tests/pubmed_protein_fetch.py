#!/usr/bin/env python3.8

# -*- coding: utf-8 -*-

import sys, os

project_path = os.path.realpath("../../")

sys.path.insert(0, project_path)

from python_eutils.esearch import ESearch
from python_eutils.elink import ELink
from python_eutils.efetch import EFetch

from python_eutils import logging

logging.getLogger().setLevel(logging.DEBUG)

##
## Test ESearch-ELink-EFetch Pipeline with a test query from
##  https://www.ncbi.nlm.nih.gov/books/NBK25497/?report=classic
##
## ``Download protein FASTA records linked to abstracts published 
## in 2009 that are indexed in MeSH for both asthma and 
## leukotrienes.''
##
##

query = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'

if __name__ == "__main__":
    
    es = ESearch(query, db='pubmed')

    if not es:
        logging.error("ESEARCH")
        sys.os.exit(1)

    logging.info(es)

    el = ELink("protein", dbfrom="pubmed", source=es)
        
    if not el:
        logging.error("ELINK")
        sys.os.exit(2)

    logging.info(el)

    ef = EFetch('pubmed', rettype='fasta', retmode='xml', source=el)

    if not ef:
        logging.error("EFETCH")
        sys.os.exit(3)

    logging.info(ef)
    
    print(ef.results())


