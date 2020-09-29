#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import logging

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
                logging.info("LOG] Setting colored format")
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

defaultquery = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'

if __name__ == "__main__":
    
    query = 'asthma[mesh]+' 

    results = efetch(query)
        
    print(results)
