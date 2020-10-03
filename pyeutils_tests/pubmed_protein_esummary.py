#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import sys, os

from python_eutils.esearch import ESearch
from python_eutils.elink import ELink
from python_eutils.esummary import ESummary

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
## Request the DocSummary of the research
##

query = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'

if __name__ == "__main__":

    search = ESearch(query, db="pubmed")

    if not search:
        logging.error("ESEARCH")
        sys.os.exit(1)
 
    linker = ELink("protein", dbfrom="pubmed", cmd="neighbor_history", source=search)

    if not linker:
        logging.error("ELINK")
        sys.os.exit(2)

    results = linker.results()

    logging.debug(f"ELINK results : {results}")

    esum = ESummary(db="protein", source=linker)

    if not esum:
        logging.error("EFETCH")
        sys.os.exit(3)

    print(esum.results())   


