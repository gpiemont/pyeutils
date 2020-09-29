# -*- coding: utf-8 -*-

from enum import Enum

class state(Enum):
    """
    EUtils Pipeline status codes
    """

    NONE        = 0
    ESEARCH     = 1
    ELINK       = 2
    ESUMMARY    = 3
    EFETCH      = 4
    EPOST       = 5

