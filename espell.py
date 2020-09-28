# -*- coding: utf-8 -*-

from . import logging

import requests

class ESpell(object):

    """
    · Provides spelling suggestions for terms within a single text query in a given database.
    """

    # Search Endpoint

    _ep7 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi';

    def __init__(self, term, db="pubmed"):
      
        self._term      = term
        
        self._espell_payload = {
            "term"        : term,
            "db"          : db
        }

        self._db        = db

        self._params    = "&".join([f"{k}={v}" for k, v in self._espell_payload.items()])

        self._results   = ""

        logging.info(f"[OBJECTS:ESPELL]   Checking for spelling suggestion of '{term}' in '{db}' ..")

    def _get_results(self, *args, **kwargs):

        response = requests.Response()

        try:
            if len(self._term) > 100:
                response = requests.post(self._ep7, self._params)
            else: 
                response = requests.get(self._ep7, self._params)

            if response.status_code != 200:
                logging.error(f"EGQuery did not complete successfully (HTTP {response.status_code})")
                return ""

            self._results   = response.text                            

        except Exception as e:
            logging.error(f"{str(e)}")
            self._results = f"{str(e)}"

        return self._results


    def results(self):
                   
        return self._get_results()


all = [ ESpell ]

