# -*- coding: utf-8 -*-

from enum import Enum

class state(Enum):
    """
    EUtils Pipeline statuses

    XXX Not every ERequests follows the same order.
    So State orders should not always be sequential.

    """

    NONE        = 0
    ESEARCH     = 1
    ELINK       = 2
    ESUMMARY    = 3
    EFETCH      = 4
    EPOST       = 5

