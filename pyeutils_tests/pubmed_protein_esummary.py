#!/usr/bin/env python3.8
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
# -*- coding: utf-8 -*-
#

import sys, os

sys.path.insert(0, "../")
sys.path.insert(0, "./")

from pyeutils.esearch import ESearch
from pyeutils.elink import ELink
from pyeutils.esummary import ESummary

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


