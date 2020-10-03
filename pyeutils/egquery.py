# -*- coding: utf-8 -*-

from . import logging

import requests

class EGQuery(object):

    """
    · Provides the number of records retrieved in all Entrez databases by a single text query.
    """

    # Search Endpoint

    _ep6 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi';

    def __init__(self, term):
      
        self._term      = term
        
        self._eg_payload = {
            "term"        : term,
        }

        self._params    = "&".join([f"{k}={v}" for k, v in self._eg_payload.items()])

        self._results   = ""

        logging.info(f"[OBJECTS:EGQUERY]   Requesting for '{term}' in all Entrez dbs..")

    def _get_results(self, *args, **kwargs):

        response = requests.Response()

        try:
            response = requests.get(self._ep6, self._params)

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


all = [ EGQuery ]

