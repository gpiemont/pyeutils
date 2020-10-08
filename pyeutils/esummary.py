# -*- coding: utf-8 -*-

from . elink import ELink
from . esearch import ESearch

from . import state, logging
import requests

class ESummary(ELink, ESearch):

    """
    ESummary class object:

    Instantiate a new ESummary request to NCBI's Entrez database

    From ``The E-Utilities In-Depth`` :
        [ https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_ESummary_ ]

    · Returns document summaries (DocSums) for a list of input UIDs
    · Returns DocSums for a set of UIDs stored on the Entrez History server

    """

    _ep2 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'

    def __init__(self, db="pubmed", ids=[], querykey=None, webenv=None, source=None,
        retstart=1, retmax=10000, retmode="xml", version="2.0"):

        self._webenv    = webenv
        self._querykey = webenv

        self._ids       = ids
        self._db        = db

        if source:

            #
            # If a previous request source is available, initaliaze ESummary request's payload 
            # with an already initalized one (ELink or ESearch) and its previous Web Environment
            #

            if isinstance(source, ELink):
                super(self.__class__, self).__init__(source._db, source._dbfrom,
                    source._cmd, source._linkname, source._ids, source._idtype, 
                    source._retmode, source._webenv, source._querykey,
                    source._datetype, source._reldate, source._minmaxdate)
                
                ##
                ## Initialize ESearch part of <self>, from source type (ESearch)
                ##

                self._term = source._term
                self._usehistory = source._usehistory

                self._results = super(self.__class__, self)._get_elinks()

                self._esummary_payload = {
                        "db"        : source._db,
                        "query_key" : source._querykey,
                        "WebEnv"    : source._webenv,
                }
    
            elif isinstance(source, ESearch):
                super(self.__class__, self).__init__(source._term, source._db, source._usehistory,
                    source._webenv, source._querykey)

                self._querykey  = source._querykey
                self._webenv    = source._webenv

                self._results = super(self.__class__, self)._get_results()

                self._esummary_payload = {
                        "db"        : source._db,
                        "query_key" : source._querykey,
                        "WebEnv"    : source._webenv,
                }

            else:
                raise Exception("source must be any in ESearch, ELinker, EPost")

        else:
                self._esummary_payload = {
                        "db"   : db,
                }

                if ids:
                        self._esummary_payload["id"] = ",".join([str(i) for i in ids])

                if webenv:
                        self._esummary_payload["webenv"] = webenv
                
                if querykey:
                        self._esummary_payload["query_key"] = query_key

        
        self._retstart  = self._esummary_payload["retstart"] = retstart
        self._retmode   = self._esummary_payload["retmode"]  = retmode
        self._retmax    = self._esummary_payload["retmax"]   = retmax
        self._version   = self._esummary_payload["version"]  = version        

        
        logging.debug(self._esummary_payload)

        self._summary_params    = "&".join([f"{k}={v}" for k, v in self._esummary_payload.items()])
        self._summary           = "" 

    def _get_summary(self, *args, **kwargs):
        
        """
        Request a Summary from the Initialization Object

        """

        response = None

        try:
            logging.debug(f"Requesting Summary URL {self._ep2}?{self._summary_params}")

            response = requests.get(self._ep2, self._summary_params)

            if response.status_code != 200:
                logging.error(f"ESummary request did not complete successfully (HTTP {response.status_code})")
                return ""
   
            self._summary   = response.text
            self._status    = state.ESUMMARY

        except Exception as e:
            logging.error(f"{str(e)}")
            self._summary = ""

        return self._webenv, self._querykey, response.text

    def results(self):

        """
        Return results from EFetch operation

        """

        try:
            self._webenv, self._querykey, self._summary = self._get_summary()

        except Exception as e:
            logging.error(f"{str(e)}")
            pass

        return self._summary

    def webenv(self):
        return self._webenv

    def querykey(self):
        return self._querykey

##
## Convenience/Pipelined Functions
##

def esearch_elink_esummary(query, dbfrom="pubmed", dbto="protein", cmd="neighbor_history"):

    """
    Return a Summary of cross-db linked results, from a given query

    Parameters:
        
        query   : str     The initial query, will be feeded to an ESearch object to perform a
                          search on ``dbfrom``

        dbfrom  : str     Perform query lookup in this DB
        dbto    : str     Retrieve results from this DB

        cmd     : str     Perform this Link operation between DBs (default : neighbor_history)

    """
    
    search = ESearch(query, db=dbfrom)

    if not search:
        return { "error" : "ESEARCH" }
 
    linker = ELink(dbto, dbfrom=dbfrom, cmd=cmd, source=search)

    if not linker:
        return { "error" : "ELINK" }

    results = linker.results()

    logging.debug(f"ELINK results : {results}")

    if not linker:
        return { "error" : "ELINK" }

    s = ESummary(db=dbfrom, source=linker)

    if not s:
        return { "error" : "ESUMMARY" }

    return s.results()

all = [ ESummary, esearch_elink_esummary ]

