#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
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


import logging

EUTILS_APPNAME  = "pyeutils"

from . ecit import *
from . ecitmatch import *
from . efetch import *
from . egquery import *
from . einfo import *
from . elink import *
from . epost import *
from . esearch import *
from . espell import *
from . esummary import *
from . eresults import *

def log_setup(linefmt='%(levelname)s: %(asctime)s : %(message)s', datefmt='%H:%M:%S',
        loglevel=logging.DEBUG):

        """
        Setup system logger with a given line format, date format and loglevel,
        optionally using colored loglines if available.

        """

        formatter = handler = None

        import os, logging

        logging.basicConfig(
            format=linefmt,         
            level=loglevel
        )

        try:
            if os.isatty(2):
                import colorlog
                logging.info("[LOG] Setting colored format")
                cformat = '%(log_color)s' + linefmt
                formatter = colorlog.ColoredFormatter(cformat, datefmt,
                      log_colors = { 'DEBUG'   : 'cyan',       'INFO' : 'bold_green',
                                     'WARNING' : 'yellow',     'ERROR': 'red',
                                     'CRITICAL': 'bold_red' })
                
        except:
                logging.info("[LOG] Setting default format")
                formatter = logging.Formatter(fmt=linefmt, datefmt=datefmt)
        
        handler = logging.StreamHandler()        
        handler.setFormatter(formatter)

        logging.getLogger().handlers = [ handler ]
        logging.getLogger().propagate = False

try:
    log_setup(loglevel=logging.INFO)
except Exception as e:
    print(str(e))
    os.exit(4)

