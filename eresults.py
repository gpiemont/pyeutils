# -*- coding: utf-8 -*-

class Eresults(object):

    """
    Results Handler class:
    Store supplied results, in XML or HTML format, and make them available as prettified text or
    as python SOUP Objects, where requested.

    """

    def __init__(self, results, format='native'):

        self._format  = format

        from bs4 import BeautifulSoup as BS4
        soup = None

        if format == 'soup':
                #
                # Keep results in soup format if requested,
                # parsing them over XML by default
                #
                try:
                    soup = BS4(self._results, "lxml")
                except:
                    soup = BS4(self._results, "html.parser")
                
                self._results = soup        
        else:
                self._results = results

    def __str__(self):

        if self._results:

            try:
                return self._results.prettify()
            except:
                return str(self._results)

        return ""
