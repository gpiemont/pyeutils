#!/usr/bin/env python3.8
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

defaultquery1 = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'
defaultquery2 = 'asthma[mesh]+AND+2019[pdat]' 
defaultquery3 = 'leukotrienes[mesh]+AND+2019[pdat]' 

queries = [
    defaultquery1,
    defaultquery2,
    defaultquery3
]

from efetch import esearch_elink_efetch as efetch1

import sys

def main(args=[]):
   
    global queries, defautquery1
    queryno = -1

    if args:
        try:
            queryno = int(args[0])
        except:
            pass

    if queryno != -1:
        results = efetch1(defaultquery1)
        print(results)
        
        return 0

    for n, q in enumerate(queries):
        results = efetch1(q)
        print(results)

    return 0

if __name__ == "__main__":

    ret = main(args=sys.argv[1:])

    sys.exit(ret)
