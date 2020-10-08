# -*- coding: utf-8 -*-

from . import EUTILS_APPNAME
from . epipe import state
from . elink import ELink
from . esearch import ESearch
from . epost import EPost

from . import logging
import requests

class EFetch(ELink, EPost, ESearch):

    """
    EFetch Class object:

    Instantiate a new EFetch operation to be performed on NCBI's Entrez database.

    From ``The E-Utilities In-Depth`` :
        [ https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch ]

    · Returns formatted data records for a list of input UIDs
    · Returns formatted data records for a set of UIDs stored on the Entrez History server

    
    Extra Features of the implementation: 
        · Try to supports operation pipelining via multiple intheritance.
        · (TODO) Authenticated API requests
    """

    _ep3 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    _querykey = ""
    _webenv   = ""

    def __init__(self, db, ids=[],          
                querykey=None, webenv=None, rettype='fasta', retmode='text',
                strand="", seq_start=0, seq_stop=0, complexity=-1,
                source=None):

        """
        Initialize an EFetch object.

        Required parameters:

        db              : Retrieve records from this Entrez db (default: 'pubmed')
                          See https://www.ncbi.nlm.nih.gov/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly
                          for supported DBs

        Required parameters - Used only when input is from an UID (``ids``) list
        
        ids             : List of UIDs or GI numbers

        usehistory      : Post search results directly to an History server and make them available
                          to a further E-request call via a WebEnv/QueryKey window.

        Required Parameters – Used only when input is from the Entrez History server

        WebEnv          : Web Environment returned from a previous E-request call. Results of the 
                          current search will be appended to this Environment.
        
        querykey        : Specify which sets of UIDs (from a previous ESearch,
                          EPost, ELink call) will be used as input to EFetch.

        See https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_EFetch_ for a complete documetation.


        Implementation Parameters:
        
        source           : Use ``source`` as an Operational Superclass for EFetch:

                                search = ESearch("<query>", db="pubmed") << Instantiate an ESearch Operation
                                fetch  = Efetch("pubmed", source=search) << Instantiate an EFetch Operation, relying on ``search`` results

                                results = fetch.results() << Sequentially executes ``search`` and ``fetch``.
 
                            N.B.: Current Pipeline status can be retrieved via ``self._status``. 
        """
       
        self._db = db
        self._ids = ids
        
        self._querykey = querykey
        self._webenv   = webenv

        self._status    = state.EFETCH

        if source:
                # Initialize Base Class from ``source``
                import time

                if type(source) == ELink:

                        super(self.__class__, self).__init__(source._db, source._dbfrom,
                                source._cmd, source._linkname, source._ids, source._idtype,
                                source._retmode, source._webenv, source._querykey,
                                source._datetype, source._reldate, source._minmaxdate)

                        self._querykey  = source._querykey
                        self._webenv    = source._webenv
                      
                        self._ids       = source._ids
 
                        ##
                        ## Initialize ESearch part of <self>, from source type (ESearch)
                        ##

                        self._term = source._term
                        self._usehistory = source._usehistory

                        logging.info(f"[OBJECTS:EFETCH] Initializing from ELink Object (WebEnv: {self._webenv}, QueryKey: {self._querykey})") 
                        self._webenv, self._querykey, self._results = super(self.__class__, self)._get_elinks()
                        
                        #super(source.__class__, self).__init__(source._term, source._db, source._usehistory,
                        #                    source._webenv, source._querykey)

                        #
                        # Sleep for 1 second between requests, as the Entrez systems does not support
                        # more than 3 unauthenticated request per second.
                        #

                        time.sleep(1)

                elif type(source) == ESearch:
                        super(self.__class__, self).__init__(source._term, source._db, source._usehistory,
                                    source._webenv, source._querykey)

                        self._querykey  = source._querykey
                        self._webenv    = source._webenv
                        self._term      = source._term

                        logging.info(f"[OBJECTS:EFETCH] Initializing from ELink Object (WebEnv: {self._webenv}, QueryKey: {self._querykey})") 
                        self._webenv, self._querykey, self._results = super(self.__class__, self)._get_results()

                        time.sleep(1)
                
                elif type(source) == EPost:
                        super(self.__class__, self).__init__(source._db, source._ids, source._webenv,
                                    source._querykey)

                        self._querykey  = source._querykey
                        self._webenv    = source._webenv
                        
                        logging.info(f"[OBJECTS:EPost] Initializing from EPost Object (WebEnv: {self._webenv}, QueryKey: {self._querykey})") 
                        self._webenv, self._querykey, self._results = super(self.__class__, self)._get_results()
                
                        time.sleep(1)
                else:
                        raise Exception("Only instances of ELink, EPost or ESearch are supported as EFetch superclass")

        else:
                if querykey or webenv:
                        # Already have a History Server environment, use `db` param as target db
                        self._db = db

        self._efetch_payload = {
                "tool"      : EUTILS_APPNAME,
                "db"        : self._db,
                "rettype"   : rettype,
                "retmode"   : retmode,
        }

        #
        # Initialize EFetch payload according to EFetch parameters
        #

        if ids:
                self._efetch_payload["id"] = ",".join([str(i) for i in ids])

        if self._querykey:
                self._efetch_payload["query_key"] = self._querykey

        if self._webenv:
                self._efetch_payload["WebEnv"] = self._webenv

        if strand:
                self._efetch_payload["strand"] = self._strand = strand

        if seq_start:
                self._efetch_payload["seq_start"] = self._seq_start = seq_start

        if seq_stop:
                self._efetch_payload["seq_stop"] = self._seq_stop = seq_stop

        if complexity > -1:
                self._efetch_payload["complexity"] = self._complexity = complexity

        logging.debug(f"EFETCH payload : {self._efetch_payload}")

        self._efetch_params    = "&".join([f"{k}={v}" for k, v in self._efetch_payload.items()])
        self._fetchdata       = "" 

        
        if not self._webenv and not self._querykey and not self._ids:
                if self._status in (state.NONE, state.ESEARCH):
                # If pipeline is in state.ESEARCH status, with no querykey/webenv set, it means that
                # some needed parameter's been not supplied. 
                # Otherwise no results have been found.                
                        raise Exception(f"Supply input as a list of UIDs (`ids` argument) or " 
                                "as a previous Web Environment/QueryKey search window " 
                                "(`querykey` and `webenv` arguments)")
                        

    def get(self, *args, **kwargs):

        """
        Perform an EFetch operation, with the supplied initialization parameters

        """

        response = requests.Response()

        try:
            self._efetch_url = f"{self._ep3}?{self._efetch_params}"
            logging.debug(f"Fetching results via efetch URL {self._efetch_url}")

            response = requests.get(self._ep3, self._efetch_params)

            if response.status_code != 200:
                logging.error(f"[OBJECTS:EFETCH] EFetch did not complete successfully (HTTP {response.status_code} : {response.reason})")
                errmsg = response.text.replace("\n", " ")
                logging.error(f"[OBJECTS:EFETCH] Error Message : {errmsg}")
                return ""
   
            self._fetchdata = response.text
            self._status    = state.EFETCH

        except Exception as e:
            import traceback as tb
            logging.error(f"{tb.format_exc()}")
            self._fetchdata = response.text

        return self._webenv, self._querykey, response.text

    def results(self):

        """
        Return results from EFetch operation

        """

        try:
            _, _, self._fetchdata = self.get()
        except ValueError:
            logging.info(f"No results found for {str(self)}")
        except Exception as e:
            import traceback as tb
            logging.error(f"{tb.format_exc()}")            

        return self._fetchdata

    def webenv(self):
        return self._webenv

    def querykey(self):
        return self._querykey

    def __repr__(self):
       
        """
        Experimental version of __repr__

        """
 
        reprs = []

        if isinstance(self, ESearch):
            if self._status.value >= state.ESEARCH.value:
                term = self._term
                reprs.append(f"ESearch<'{term}', {self._dbfrom}'>")

        if isinstance(self, ELink):
            if self._status.value >= state.ELINK.value:             
                 reprs.append(f":ELink<'{self._dbfrom}', '{self._db}'>")
        
        if isinstance(self, EPost):  
            if self._status.value >= state.EPOST.value:
                 reprs.append(f":EPost<'{self._db}', '{len(self._ids)}'>")

        reprs.append(f"EFetch<'{self._db}', '{len(self._ids)}'>")

        self._repr = ":".join(reprs)

        return self._repr

##
## Pipelined functions
##

def esearch_elink_efetch(query, dbfrom="pubmed", dbto="protein", 
        cmd="neighbor_history", rettype='fasta', retmode='text'):

    """
    Experimental.

    Perform an EFetch Operation after an ELink and ESearch

    query   : str (opt)
        Textual query to feed to ELink
    
    dbfrom  : str (opt)
        Database with the input UIDs (Origin database of the link op)
        
    """

    esearch  = ESearch(query, db=dbfrom, rettype=rettype,
                      retmode="xml")

    if not esearch:
        return { "error" : "ESEARCH" }

    elink   = ELink(dbto, dbfrom=dbfrom, retmode="xml",
                   cmd=cmd, source=esearch)

    if not elink:
        return { "error" : "ELINK" }

    fetch   = EFetch(dbfrom, rettype=rettype, retmode=retmode,
                    source=elink)
               
    if not fetch:
        return { "error" : "EFETCH" }

    return fetch.results()

def esearch_elink_efetch_xml(query, dbfrom="pubmed", dbto="protein", cmd="neighbor_history",
        rettype='fasta'):

    return esearch_elink_efetch(query, dbfrom=dbfrom, dbto=dbto, cmd=cmd, rettype=rettype, retmode='xml')

def esearch_elink_efetch_asn1(query, dbfrom="pubmed", dbto="protein", cmd="neighbor_history",
        rettype='fasta'):

    return esearch_elink_efetch(query, dbfrom=dbfrom, dbto=dbto, cmd=cmd, rettype=rettype, retmode='asn.1')

all = [ EFetch, esearch_elink_efetch, esearch_elink_efetch_xml, esearch_elink_efetch_asn1 ]

