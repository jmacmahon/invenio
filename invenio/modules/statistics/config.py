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

STATS_CFG = {
    "events": {
        "pageviews": {
            "source": "elasticsearch",
            "params": {
                "doc_type": "events.pageviews",
                "rec_id_field": "id_bibrec"
            },
            "statistics": {
                "timeline": {
                    "query_type": "histogram",
                    "display": "timeline",
                    "field": "@timestamp"
                },
                "by_ip": {
                    "query_type": "terms",
                    "display": "pie",
                    "field": "client_host"
                },
                "by_user": {
                    "query_type": "terms",
                    "display": "pie",
                    "field": "id_user"
                }
            },
            "title": "Pageviews"
        },
        "downloads": {
            "source": "elasticsearch",
            "params": {
                "doc_type": "events.downloads",
                "rec_id_field": "id_bibrec"
            },
            "statistics": {
                "timeline": {
                    "query_type": "histogram",
                    "display": "timeline",
                    "field": "@timestamp"
                }
            },
            "title": "Downloads"
        }
    }
}
