# -*- coding: utf-8 -*-

class ECit(object):

        """
        Construct an ECit Object representing a citation or a citation set.

        """

        def __init__(self, title, year, volume, first_page, author, key):
                """
                Initialize a Citation Object according to 
                https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_ECitMatch_

                [...]
                Citation strings. Each input citation must be represented by a citation string in the following format:
                journal_title|year|volume|first_page|author_name|your_key|

                [...]

                Ensure that all spaces are converted to '+' (plus-quoted)

                """

                #
                # Contains Raw citation bdata. We could have used a set(), but we want to preserve
                # arrival order
                #
 
                self._bdata = []

                title_expr = title.replace(' ', '+')
                author_expr = author.replace(' ', '+')

                obj = "|".join([f"{title_expr}", f"{year}", f"{volume}", f"{first_page}", f"{author_expr}", f"{key}"])

                self._bdata.append(obj)

        def __add__(self, other):
                
                """
                Add two ECit objects to form a citation set

                """

                if other._bdata not in self._bdata:
                    #
                    # Citation data are stored sequentially
                    #
                    self._bdata.append(other._bdata)

        def __str__(self):
                """
                Return a string representing the citation query (self._bdata)
                """

                return "\n".join(self._bdata)

        def __repr__(self):
                """
                See above. 
                """

                return self.__str__()

all = [ ECit ]
