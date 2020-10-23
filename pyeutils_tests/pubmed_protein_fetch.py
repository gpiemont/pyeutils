#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018-2020 Giulio Piemontese <gpiemont [at] protonmail.com>
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys, os

from pyeutils.esearch import ESearch
from pyeutils.elink import ELink
from pyeutils.efetch import EFetch

from pyeutils import logging

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
    
    es = ESearch(query, db='pubmed', retmode="xml")

    if not es:
        logging.error("ESEARCH")
        sys.os.exit(1)

    logging.info(es)

    el = ELink("protein", dbfrom="pubmed", retmode="xml", cmd="neighbor_history", source=es)
        
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


