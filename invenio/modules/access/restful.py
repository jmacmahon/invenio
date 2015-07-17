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

from functools import wraps

from flask import request
from flask_restful import Resource, abort
from invenio.ext.restful import require_api_auth, require_oauth_scopes
from invenio.modules.oauth2server.models import Scope
from invenio.modules.oauth2server.registry import scopes
from .engine import acc_authorize_action


class PermissionsResource(Resource):
    @require_api_auth()
    @require_oauth_scopes('access:permissions')
    def get(self, permission):
        uid = request.oauth.access_token.user_id
        authorized = acc_authorize_action(uid, permission)
        return {
            'permitted': authorized[0] == 0,
            'message': authorized[1],
            'permission': permission,
            'uid': uid
        }


def setup_app(app, api):
    api.add_resource(
        PermissionsResource,
        '/api/permissions/<permission>'
    )

    with app.app_context():
        scopes.register(Scope(
            'access:permissions',
            help_text='Allow access to check your permissible user actions.',
            internal=True
        ))
