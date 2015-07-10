# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from __future__ import absolute_import

__revision__ = \
    "$Id$"

from invenio.config import \
    CFG_ES_STATISTICS_LOGGING, \
    CFG_ES_STATISTICS_INDEX_PREFIX, \
    CFG_ES_STATISTICS_HOSTS, \
    CFG_ES_STATISTICS_SUFFIX_FORMAT, \
    CFG_ES_STATISTICS_MAX_QUEUE_LENGTH, \
    CFG_ES_STATISTICS_FLUSH_INTERVAL, \
    DEBUG

if CFG_ES_STATISTICS_LOGGING:
    import lumberjack
    import logging
    import sys
    import json


def initialise_lumberjack():
    if not CFG_ES_STATISTICS_LOGGING:
        return None
    config = lumberjack.get_default_config()
    config['index_prefix'] = CFG_ES_STATISTICS_INDEX_PREFIX

    if CFG_ES_STATISTICS_MAX_QUEUE_LENGTH == -1:
        config['max_queue_length'] = None
    else:
        config['max_queue_length'] = CFG_ES_STATISTICS_MAX_QUEUE_LENGTH

    if CFG_ES_STATISTICS_FLUSH_INTERVAL == -1:
        config['interval'] = None
    else:
        config['interval'] = CFG_ES_STATISTICS_FLUSH_INTERVAL

    lj = lumberjack.Lumberjack(
        hosts=CFG_ES_STATISTICS_HOSTS,
        config=config)

    handler = lj.get_handler(suffix_format=CFG_ES_STATISTICS_SUFFIX_FORMAT)
    logging.getLogger('events').addHandler(handler)
    logging.getLogger('events').setLevel(logging.INFO)

    if DEBUG:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.ERROR

    logging.getLogger('lumberjack').addHandler(
        logging.StreamHandler(stream=sys.stderr))
    logging.getLogger('lumberjack').setLevel(loglevel)

    logging.getLogger('elasticsearch').addHandler(
        logging.StreamHandler(stream=sys.stderr))
    logging.getLogger('elasticsearch').setLevel(loglevel)

    return lj

LUMBERJACK = initialise_lumberjack()
