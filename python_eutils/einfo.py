# -*- coding: utf-8 -*-

from . epipe import state
from . import logging

import requests

class EInfo(object):

    """
    EInfo Class object: 

    Gather Statistics from an Entrez database or provide a list with all available database

    From ``The E-Utilities In-Depth`` :
        [ https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EInfo ]

    · Provides a list of the names of all valid Entrez databases
    · Provides statistics for a single database, including lists of indexing fields and available link names

    """

    # Search Endpoint

    _ep5 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi';

    def __init__(self, db="", retmode="xml", version="2.0"):
      
        self._db      = db
        
        self._einfo_payload = {
            "db"        : db,
            "retmode"   : retmode,
            "version"   : version
        }

        self._params    = "&".join([f"{k}={v}" for k, v in self._einfo_payload.items()])

        self._results   = ""
        self._retmode   = retmode

        logging.info(f"[OBJECTS:EINFO]   Requesting to db : '{db}' ")
        logging.info(f"[OBJECTS:EINFO]            retmode : {self._einfo_payload['retmode']}")
        logging.info(f"[OBJECTS:EINFO]            version : {self._einfo_payload['version']}")


    def _get_results(self, *args, **kwargs):

        response = requests.Response()

        try:
            response = requests.get(self._ep5, self._params)

            if response.status_code != 200:
                logging.error(f"EInfo request did not complete successfully (HTTP {response.status_code})")
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


all = [ EInfo ]
