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
#

class EResults(object):

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
                    soup = BS4(results, "lxml")
                except:
                    soup = BS4(results, "html.parser")
                
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

all = [ EResults ]
