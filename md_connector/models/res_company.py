# -*- coding: utf-8 -*-
"""Classes extending the populate factory for Companies and related models.

Only adding specificities of basic accounting applications.
"""
from odoo import models, fields, _
from odoo.exceptions import UserError

import requests
import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    """Populate factory part for the accountings applications of res.company."""
    _name = 'res.company'
    _inherit = ["res.company", 'md_connector.abstract_request_manager']

    md_user = fields.Char(default="MD")
    md_password = fields.Char(default="TestPassword")
    md_token = fields.Char()
    authenticated = fields.Boolean()

    @property
    def is_valid_token(self) -> bool:
        self.action_authenticate()
        if self.md_token:
            return True
        else:
            return False

    @property
    def default_headres(self):
        return {'Token': self.md_token}

    def action_authenticate(self):
        """ authenticate company  via md user and password to get valid token"""
        if not all([self.md_user, self.md_user]):
            return

        payload = {
            "userid": self.md_user,
            "Password": self.md_password
        }
        response = self._send_request(payload=payload, endpoint='/mdsa/API/login.php')
        if response and response[0].get('isSuccess', False):
            self.authenticated = True
            if not self.md_token or self._context.get('refresh_token', False):
                self.md_token = response[0].get('token')
        else:
            self.authenticated = False
            self.md_token = False


