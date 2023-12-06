import requests
import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import json
import logging
import time
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class PwdConnector(models.Model):
    _name = 'pwd.connector'
    _rec_name = 'business_name'
    _description = "pwd Connector"

    business_name = fields.Char(string=_("Business Name"))
    base_url = fields.Char(default="https://md-sa.net")
    md_user = fields.Char(default="MD")
    md_password = fields.Char(default="TestPassword")
    md_token = fields.Char()
    authenticated = fields.Boolean()
    company_id = fields.Many2one(
        'res.company', 'Company', default=lambda self: self.env.company,
        readonly=True, required=True,
        help='The company is automatically set from your user preferences.')

    @property
    def is_valid_token(self) -> bool:
        self.action_authenticate()
        if self.md_token:
            return True
        else:
            return False

    @property
    def default_headers(self):
        return {'Token': self.md_token}

    def action_authenticate(self):
        """ authenticate company  via md user and password to get valid token"""
        if not all([self.md_user, self.md_user]):
            return

        payload = {
            "userid": self.md_user,
            "Password": self.md_password
        }
        response = self._send_request(payload=payload, endpoint='/mdsa/API/login.php', url=self.base_url)
        if response and response[0].get('isSuccess', False):
            self.authenticated = True
            if not self.md_token or self._context.get('refresh_token', False):
                self.md_token = response[0].get('token')
        else:
            self.authenticated = False
            self.md_token = False

    def _send_request(self, payload=False, url="https://md-sa.net", endpoint=False, headers={}) -> str:
        # base_url = self.env['ir.config_parameter'].sudo().get_param('md_connector.base_url',
        #                                                            'https://md-sa.net')
        base_url = url
        full_url = f'{base_url}{endpoint}'
        try:
            if payload and not headers:
                response = requests.post(full_url, json=payload)
            elif not payload and headers:
                response = requests.post(full_url, headers=headers)
            else:
                response = requests.post(full_url, headers=headers, json=payload)

            if response.status_code == 200:
                json_response = response.json()
                return json_response

            return False
        except Exception as e:
            _logger.error("Connection failed")
            return False

    def success_popup(self, data):
        return {
            "name": "Message",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "pop.message",
            "target": "new",
            "context": {
                "default_name": "Successfully %s Imported!" % data
            },
        }

    def get_import_users(self):

        print("hi zaki import")
        MyUsers = self.env['res.users'].sudo()
        if self.authenticated:
            last_users_id = MyUsers.search([('md_account_id', '!=', False)], order='md_account_id desc', limit=1)
            print("last_users_id ", last_users_id)
            if last_users_id:
                response = MyUsers._get_user_info(account_id=last_users_id.md_account_id + 1, myconnect=self)
            else:
                endpoint = '/mdsa/API/Rep_List.php'
                response = self._send_request(headers=self.default_headers, endpoint=endpoint)
                print("response", response)

            MyUsers._proceed_response(response=response, myconnect=self)
        return self.success_popup('Users')

    def get_info(self, payload, endpoint):
        response = self._send_request(payload=payload, headers=self.default_headers, endpoint=endpoint)
        return response
    # @api.model
    # def action_poll_res_user(self):
    #     print("hi zaki")
    #     MyUsers = self.env['res.users'].sudo()
    #     if self.is_valid_token:
    #         last_users_id = self.search([('md_account_id', '!=', False)], order='md_account_id desc', limit=1)
    #         if last_users_id:
    #             response = MyUsers._get_user_info(account_id=last_users_id.md_account_id + 1)
    #         else:
    #             endpoint = '/mdsa/API/Rep_List.php'
    #             response = self._send_request(headers=self.company.default_headres, endpoint=endpoint)
    #
    #         MyUsers._proceed_response(response)
