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

from . import logging
from . ecit import ECit

import requests

class ECitMatch(object):

    """
    · Retrieves PubMed IDs (PMIDs) that correspond to a set of input citation strings.
    """

    # Search Endpoint

    _ep8 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.fcgi';

    def __init__(self, bdata : str):
      
        self._db         = "pubmed"
        self._bdata      = str(bdata)
        self._rettype    = "xml"
        
        self._eg_payload = {
            "db"          : self._db,
            "rettype"     : self._rettype,
            "bdata"       : bdata,
        }

        self._params    = "&".join([f"{k}={v}" for k, v in self._eg_payload.items()])
        self._results   = ""

        logging.info(f"[OBJECTS:ECITMATCH]   Looking citation string set '{self._bdata}' in {self._db}..")

    def _get_results(self, *args, **kwargs):

        response = requests.Response()

        try:
            response = requests.get(self._ep8, self._params)

            if response.status_code != 200:
                logging.error(f"EGQuery did not complete successfully (HTTP {response.status_code})")
                return ""

            self._results   = response.text                            

        except Exception as e:
            logging.error(f"{str(e)}")
            self._results = f"{str(e)}"

        return self._results

    def results(self):

        if not self._results:
            self._results = self._get_results()

        return self._results


all = [ ECitMatch ]
