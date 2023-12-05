# -*- coding: utf-8 -*-


from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

import requests
import logging

_logger = logging.getLogger(__name__)


class AbstractRequestManager(models.AbstractModel):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "md_connector.abstract_request_manager"
    _description = "Abstract Code Index"
    _abstract = True

    def _send_request(self, payload=False, url="https://md-sa.net",endpoint=False, headers=0) -> str:
        # base_url = self.env['ir.config_parameter'].sudo().get_param('md_connector.base_url',
        #                                                            'https://md-sa.net')
        base_url =url
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
