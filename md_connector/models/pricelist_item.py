# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    company_price = fields.Float(default=0.0)

    @property
    def endpoint_pricelist_item_lst(self):
        return ''

    @property
    def endpoint_pricelist_item_info(self):
        return ''

    @api.model
    def action_poll_pricelist_item(self, connector):
        ...

    def _proceed_response(self):
        ...

    def _prepare_pricelist_item_vals(self, company_id):
        # {
        #     "ProductsID": "2",
        #     "Products": "SAWA GV 20SR -23SAR",
        #     "channel_name": "KDR ",
        #     "Company_Price": "0.0000",
        #     "End_User_Price": "0.0000"
        # }
        prepared_vals = {
            'name': '',
            'company_id': company_id
        }
        return prepared_vals
