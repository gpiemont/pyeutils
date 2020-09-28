# -*- coding: utf-8 -*-

from . epipe import state
from . import logging
import requests

class ESearch(object):

    """
    ESearch Class object:

    Instantiate a new search to be performed in NCBI's Entrez database.
    Also used as a base class for more complex Entrez queries, like
    ELink, EPost and EFetch

    From ``The E-Utilities In-Depth`` :
       [https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_ESearch_ ]

    · Provides a list of UIDs matching a text query
    · Posts the results of a search on the History server
    · Downloads all UIDs from a dataset stored on the History server
    ¯ Combines or limits UID datasets stored on the History server
    · Sorts sets of UIDs

    """
    # Search Endpoint

    _ep0  = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi';

    # Search Query

    _term = ""
    
    # Search DB

    _db   = "pubmed"
    
    def __init__(self, term, db="pubmed", usehistory=True, 
            webenv=None, querykey=None,
            retstart=0, retmax=20, rettype='uilist', retmode='xml', sort='',
            field='', idtype='', datetype='', reldate='', mindatemax=''):

        """
        Initialize a ESearch object to a given search ``term``

        Required parameters:

        term            : URL-encoded text query
        db              : Perform the search in this Entrez db (default: 'pubmed')


        Optional Parameters - History Server
        
        usehistory      : Post search results directly to an History server and make them available
                          to a further E-request call via a WebEnv/QueryKey window

        WebEnv          : Web Environment returned from a previous E-request call. Results of the 
                          current search will be appended to this Environment.
        
        querykey        : Intersects query string in ``term`` with a query from a previous ESearch,
                          EPost, ELink call, stored in a History Server as query_key.

        See https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_ESearch_ for a complete documetation.

        """

        self._term    = term

        self._db      = db
        self._retmode = retmode
        self._rettype = rettype
        
        self._retstart = retstart
        self._retmax  = retmax

        self._usehistory = usehistory

        self._esearch_payload = {
            "term" : term,
            "db"   : db,
            "usehistory" : "y" if usehistory else "n",
            "retmode"   : retmode,
            "rettype"   : rettype,
        }

        if webenv:
            self._esearch_payload["webenv"] = self._webenv = webenv

        if querykey:
            self._esearch_payload["query_key"] = self._querykey = querykey

        if sort:
            self._esearch_payload["sort"] = sort

        if field:
            self._esearch_payload["field"] = field

        if idtype:
            self._esearch_payload["idtype"] = idtype

        if datetype:
            self._esearch_payload["datetype"] = datetype

        if reldate:
            self._esearch_payload["reldate"] = reldate

        if mindatemax:
            self._esearch_payload["mindatemax"] = mindatemax

        self._params    = "&".join([f"{k}={v}" for k, v in self._esearch_payload.items()])
        self._objs      = {}

        self._webenv    = ""
        self._querykey  = ""
        self._results   = ""

        self._status    = state.ESEARCH

        logging.info(f"[OBJECTS:{self._status.name}]   ESearch query : '{term}'")

    def _get_results(self, *args, **kwargs):

        """
        Perform an ESearch query and return results as History Server coordinates
        (WebEnv/query_key) or full-text results

        """

        try:
            response = requests.get(self._ep0, self._params)

            if response.status_code != 200:
                logging.error(f"ESearch did not complete successfully (HTTP {response.status_code})")
                return ""

            self._status    = state.ESEARCH

            self._results   = response.text

            self._webenv    = self.parse("WebEnv")
            self._querykey  = self.parse("QueryKey", objtype=int)
            self._count     = self.parse("Count", objtype=int)
            self._retmax    = self.parse("retmax", objtype=int)
            self._retstart  = self.parse("retstart", objtype=int)
            self._ids       = self.parse("Id", objtype=list, first=False)

        except Exception as e:
            import traceback as tb
            logging.error(f"{tb.format_exc()}")
            logging.error(f"{str(e)}")
            self._results = f"{str(e)}"

        return self._webenv, self._querykey, self._results

    def parse(self, name, objtype=str, first=True):

        """
        Parse returned Parameter values from a Search result

        name  : str
                Parameter name
        
        objtype : `class type`, optional
                Python's parameter type

        first : bool, opitonal
                Return only the first occourrence of Parameter in results

        """

        try:
            from bs4 import BeautifulSoup as BS4
            from bs4 import FeatureNotFound

            soup = None

            try:
                soup = BS4(self._results, "lxml")
            except FeatureNotFound as e:
                soup = BS4(self._results, "html.parser")

            if not soup:
                raise Exception("No suitable parser found on system (xml nor html.parser)")

            objs = soup.findAll(name.lower()) if not first else soup.find(name.lower())

            if not objs:
                #if self._status == state.ESEARCH:
                #    logging.info(f"No {name} found for search object {self} (search term : '{self._term}')")

                return ""

            if objtype == list:
                self._objs[name] = [ obj.text for obj in objs ]
            elif objtype == int:
                try:
                    self._objs[name] = int(objs.text)
                except:
                    # Store it anyway as default type
                    self._objs[name] = objs
            elif objtype == float:
                try:
                    self._objs[name] = float(objs.text)
                except:
                    # Store it anyway as default type
                    self._objs[name] = objs                
            else:
                self._objs[name] = str(objs.text)

            logging.info(f"[OBJECTS:{self._status.name}] " + f"{name:>15}" +  f" : {self._objs[name]}")

        except Exception as e:
            logging.debug(f"Error in looking up {name} for search object {self} (search term : '{self._term}') : {str(e)}")

        return self._objs.get(name)

    def results(self):

        try:
            self._webenv, self._querykey, self._results = self._get_results()
        except:
            pass

        return self._results

    def webenv(self):
        return self._webenv

    def querykey(self):
        return self._querykey
 
##
## Convenience funcitons. Used also for testing purposes
##

def esearch(query, dbname="pubmed"):

    """
    Perform an ESearch query on a specified Entrez db (default: pubmed)
    """

    search = ESearch(query, db=dbname)

    return search.results()

def esearch_pubmed(query):
    """
    Perform an ESearch query directly on `pubmed` Entrez db
    """

    return esearch(query)


all = [ ESearch, esearch, esearch_pubmed ]

