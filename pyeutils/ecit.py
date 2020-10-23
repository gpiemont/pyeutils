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
