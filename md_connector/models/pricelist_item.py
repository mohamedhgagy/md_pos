# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    company_price = fields.Float(default=0.0)
    md_channel_name = fields.Char(related='pricelist_id.md_channel_name')

    @property
    def endpoint_pricelist_info(self):
        return '/mdsa/API/channel_Info.php'

    @api.model
    def action_poll_pricelist_items(self, pricelist_id, connector):
        payload = {
            "channel_name": pricelist_id.md_channel_name
        }
        response = connector._send_request(endpoint=self.endpoint_pricelist_info, payload=payload,
                                           headers=connector.default_headers)
        self._proceed_response(response, pricelist_id)

    def _proceed_response(self, response, pricelist_id):
        if response and response[0].get('isSuccess', False):
            pricelist_items = response[0].get('Channel info', []) or []
            prepared_item_list = []
            for item in pricelist_items:
                if int(item.get('ProductsID'), 0) not in pricelist_id.item_ids.mapped('product_id.md_product_id'):
                    prepared_item_list.append(self._prepare_pricelist_item_vals(item, pricelist_id))
            if prepared_item_list:
                pricelist_id.item_ids = [(0, 0, p_item) for p_item in prepared_item_list]

    def _prepare_pricelist_item_vals(self, item, pricelist_id):
        _domain_search = [('md_product_id', '=', item.get('ProductsID')), ('md_product_id', '!=', False)]
        product_tmpl_id = self.env['product.template'].sudo().search(_domain_search, limit=1)
        product_id = product_tmpl_id.product_variant_id.id
        prepared_vals = {
            'pricelist_id': pricelist_id.id,
            'product_tmpl_id': product_tmpl_id.id,
            'product_id': product_id,
            'fixed_price': item.get('End_User_Price', 0.0),
            'company_price': item.get('Company_Price', 0.0),
        }
        return prepared_vals
