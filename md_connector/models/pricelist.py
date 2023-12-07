# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    @property
    def endpoint_pricelist_lst(self):
        return ''

    @property
    def endpoint_pricelist_info(self):
        return ''

    @api.model
    def action_poll_pricelist(self, connector):
        ...

    def _proceed_response(self):
        ...

    def _prepare_pricelist_vals(self, company_id):
        prepared_vals = {
            'name': '',
            'company_id': company_id
        }
        return prepared_vals
