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

from . esearch import ESearch
from . elink import ELink
from . epipe import state 
from . import logging
import requests

class EPost(object):
    """
    EPost Class object:

    Instantiate a new EPost operation to create an operational WebEnv on NCBI Server.
        
    From ``The E-Utilities In-Depth`` :
        [ https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_EPost_ ]

    * Uploads a list of UIDs to the Entrez History server
    * Appends a list of UIDs to an existing set of UID lists attached to a Web Environment

    """

    # Search Endpoint

    _ep4 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi';

    def __init__(self, db="pubmed", ids=[], webenv=None, querykey=None,
              source=None):
      
        self._db      = db
        self._ids     = ids

        self._epost_payload = {
            "db"   : db,
            "id"   : ",".join([str(i) for i in ids]),
        }

        self._params    = "&".join([f"{k}={v}" for k, v in self._epost_payload.items()])
        self._objs      = {}

        if source and isinstance(source, (ESearch, EPost, ELink)):
                self._webenv    = source._webenv
                self._querykey  = source._querykey
        else:
                self._webenv    = webenv
                self._querykey  = querykey

        self._results   = ""

        self._status    = state.EPOST

        logging.info(f"[OBJECTS:{self._status.name}]   Requesting to db : '{db}' ")
        logging.info(f"[OBJECTS:{self._status.name}]   Requesting IDs   : {self._epost_payload['id']}")

    def _get_epost_results(self, *args, **kwargs):

        try:
            response = requests.Response()

            if len(self._ids) < 200:
                response = requests.get(self._ep4, self._params)
            else:
                response = requests.post(self._ep4, self._params)

            if response.status_code != 200:
                logging.error(f"EPost did not complete successfully (HTTP {response.status_code})")
                return ""            

            self._results   = response.text
                            
            self._webenv    = self.parse("WebEnv")
            self._querykey  = self.parse("QueryKey", objtype=int)

            self._status    = state.EPOST

        except Exception as e:
            logging.error(f"{str(e)}")
            self._results = f"{str(e)}"

        return self._webenv, self._querykey, self._results


    def results(self):

        try:
            self._webenv, self._querykey, self._results = self._get_epost_results()
        except:
            pass

        return self._results

    def webenv(self):
        return self._webenv

    def query_key(self):
        return self._querykey

all = [ EPost ]
