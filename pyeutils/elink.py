# -*- coding: utf-8 -*-

from . evars import EUTILS_APPNAME
from . epipe import state
from . esearch import ESearch
from . import logging

import requests

class ELink(ESearch):

    """
    ELink Class object:

    Perform a Link operation between two sets of UIDs in two Entrez DBs following different command modes

        From ``The E-Utilities In-Depth`` :
                [ https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_ELink_ ]

    · Returns UIDs linked to an input set of UIDs in either the same or a different Entrez database
    · Returns UIDs linked to other UIDs in the same Entrez database that match an Entrez query
    · Checks for the existence of Entrez links for a set of UIDs within the same database
    · Lists the available links for a UID
    · Lists LinkOut URLs and attributes for a set of UIDs
    · Lists hyperlinks to primary LinkOut providers for a set of UIDs
    · Creates hyperlinks to the primary LinkOut provider for a single UID


    Extra Features of the implementation: 
        · Try to supports operation pipelining via multiple intheritance.
        · (TODO) Authenticated API requests

    """

    _ep1 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'

    def __init__(self, db="pubmed", dbfrom="pubmed", cmd="neighbor",
                linkname=None, ids=[], idtype='',
                retmode='xml', webenv=None, querykey=None,
                holding='',
                datetype='', reldate=None, minmaxdate='',
                source=None):

        """
        Initialize an ELink object.

        Required parameters:

        db              : Retrieve UIDs from this Entrez db (default: 'pubmed')
                          (target of the link)

        dbfrom          : Origin database for the link operation. If equal to ``db``
                          computational neighbours in the db will be returned. 
                          See https://eutils.ncbi.nlm.nih.gov/entrez/query/static/entrezlinks.html for a list of all, per-db, computational neighbour

        
        cmd             : Command mode. Specifies which kind of function ELink will
                          perform (determining how the UIDs will be liked between DBs).
                          Default : 'neighbor'

        See https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_ELink_ for a complete documentation.


        Implementation Parameters:
        
        source           : Use ``source`` as an Operational superclass for ELink:

                                search = ESearch("<query>", db="pubmed") << Instantiate a ESearch Operation
                                link   = ELink("protein", dbfrom="pubmed", source=es) << Instantiate an ELink Operation, relying on ``search`` results
              
                                results = link.results() << Sequentially executes ``search`` and ``link``.
 
                            N.B.: Current Pipeline status can be retrieved via ``self._status``. 
        """

        self._querykey = querykey
        self._webenv   = webenv
     
        if source:
                if isinstance(source, ESearch):
                        super(self.__class__, self).__init__(source._term, source._db, source._usehistory,
                                source._webenv, source._querykey, source._retstart, source._retmax)
                                       
                        self._webenv   = source._webenv
                        self._querykey = source._querykey
                else:
                        raise Exception("Only instances of ESearch is supported as ELink superclass, atm.")

        self._dbfrom    = dbfrom
        self._db        = db

        self._linkname  = linkname or f"{dbfrom}_{db}"
        self._cmd       = cmd

        self._idtype     = idtype
        self._datetype   = datetype
        self._reldate    = reldate
        self._minmaxdate = minmaxdate

        if source:
            if not querykey or not webenv:
                    import time
                    try:
                        # Gather results from base class (the ESearch object, ndr)
                        self._webenv, self._querykey, self._results = super(self.__class__, self)._get_results()
                        time.sleep(1)
                    except Exception as e:
                        raise Exception(f"Error in ELink initialization : {str(e)}")

        self._retmode       = retmode

        self._elink_payload = {
                "dbfrom"    : self._dbfrom,
                "db"        : self._db,
                "linkname"  : self._linkname,
                "cmd"       : self._cmd,
                "retmode"   : self._retmode,
                "tool"      : EUTILS_APPNAME
        }

        if self._querykey: 
            self._elink_payload["query_key"] = self._querykey

        if self._webenv:
            self._elink_payload["WebEnv"] = self._webenv

        if ids:
            self._elink_payload["id"] = ",".join([str(i) for i in ids])

        if idtype:
            self._elink_payload["idype"] = idtype

        if cmd in ('llinks', 'llinkslib') and holding:
            self._elink_payload["holding"] = holding
            
        if datetype:
            self._elink_payload["datetype"] = datetype
            
        if reldate:
            self._elink_payload["reldate"] = reldate

        if minmaxdate:
            self._elink_payload["minmaxdate"] = minmaxdate

        import json

        if "history" in self._cmd and not self._webenv and not self._querykey:
            logging.warning(f"[OBJECTS:ELINK] Requested ELink cmd={self._cmd} requires data from History Server, "
                                "but not WebEnv or query_key have been set.")
        
        if self._webenv and self._querykey and not "history" in self._cmd:
            logging.warning(f"[OBJECTS:ELINK] WebEnv and query_key have been set, but requested ELink (cmd={self._cmd}) "
                                "does not require them. Further responses can be empty.")

        logging.debug(f"ELINK Payload : {json.dumps(self._elink_payload, indent=4)}")

        self._params    = "&".join([f"{k}={v}" for k, v in self._elink_payload.items()])
        self._objs      = {}
    
    def _get_elinks(self, *args, **kwargs):

        try:
            logging.debug(f"Requesting ELINKS URL {self._ep1}?{self._params}")

            response = requests.get(self._ep1, self._params)

            if response.status_code != 200:
                logging.error(f"ELink request did not complete successfully (HTTP {response.status_code} : {response.reason})")
                logging.error(f"ELink error message : {response.text}")
                return ""
    
            self._results   = response.text
            self._status    = state.ELINK
            
            webenv   = self.parse("WebEnv")
            querykey = self.parse("QueryKey", objtype=int)  
         
            if webenv:
                # If there's a new WebEnv
                self._webenv = webenv

            if querykey:
                # If there's a new querykey
                self._querykey = querykey

            if webenv and not querykey:
                logging.warning(f"[OBJECTS:ELINK] ELink [{self._dbfrom} ==> {self._db}] has no QueryKey, further operations (EFectch, ESummary) will not be possible.")
                
        except Exception as e:
            import traceback as tb
            logging.error(f"{tb.format_exc()}")
            logging.error(f"{str(e)}")
            self._results = f"{str(e)}"

        return self._webenv, self._querykey, self._results

    def results(self):

        try:
            _, _, self._results = self._get_elinks()

        except Exception as e:
            import traceback as tb
            logging.error(f"{tb.format_exc()}")
            logging.error(f"{str(e)}")
            pass

        return self._results


    def webenv(self):
        return self._webenv

    def querykey(self):
        return self._querykey

def elink(query, fromdb="pubmed", todb="protein", cmd="neighbor"):

    """
    ELink returns a set of UIDs in db linked to the input UIDs in dbfrom.

    Example: Link from protein to gene

    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=gene&id=15718680,157427902

    """

    linker = ELink(query, db=todb, dbfrom=fromdb, cmd=cmd)

    return linker.results()
    
def elink_nh(query, fromdb, todb):

    """
    ELink posts the output UIDs to the Entrez History server and returns a query_key and WebEnv corresponding to the location of the output set.

    Example: Link from protein to gene and post the results on the Entrez History

    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=gene&id=15718680,157427902&cmd=neighbor_history

    """

    return elink(query, fromdb=fromdb, db=todb, cmd="neighbor_history")

def elink_ns(query, fromdb, todb):

    """
    ELink returns a set of UIDs within the same database as the input UIDs along with computed similarity scores.

    Example: Find related articles to PMID 20210808

    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=20210808&cmd=neighbor_score

    """

    return elink(query, fromdb=fromdb, todb=todb, cmd="neighbor_score")

def elink_acheck(query, fromdb, todb):

    """
    ELink lists all links available for a set of UIDs.

    """

    return elink(query, fromdb=fromdb, todb=todb, cmd="acheck")

def elink_lcheck(query, fromdb, todb):

    """
    Example: List all possible links from two protein GIs to PubMed

    """

    return elink(query, fromdb=fromdb, todb=todb, cmd="lcheck")

def elink_ncheck(query, fromdb, todb):

    """
    ELink checks for the existence of links within the same database for a set of UIDs. 
    These links are equivalent to setting db and dbfrom to the same value.

    """

    return elink(query, fromdb=fromdb, todb=todb, cmd="ncheck")

def elink_llinks(query, fromdb, todb):
    
    """
    For each input UID, ELink lists the URLs and attributes for the LinkOut providers that are not libraries.

    """

    return elink(query, fromdb=fromdb, todb=todb, cmd="llinks")


all = [ ELink, elink, elink_nh, elink_ns, elink_acheck, elink_lcheck, elink_lcheck, elink_ncheck, elink_llinks ]

