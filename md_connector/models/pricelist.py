# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Pricelist(models.Model):
    _inherit = "product.pricelist"
    _sql_constraints = [('md_channel_name', 'unique (md_channel_name)', "MD channel name should be unique")]
    md_channel_name = fields.Char(string='Channel name')

    @property
    def endpoint_pricelist_lst(self):
        return '/mdsa/API/channel_List.php'

    @property
    def endpoint_pricelist_info(self):
        return 'mdsa/API/channel_Info.php'

    @api.model
    def action_poll_pricelist(self, connector):

        response = connector._send_request(endpoint=self.endpoint_pricelist_lst, headers=connector.default_headers)
        self._proceed_response(response, connector)

    def _proceed_response(self, response, connector):
        if response and response[0].get('isSuccess', False):
            pricelists = response[0].get('Channel Name', []) or []
            if pricelists:
                prepared_priceslists = []
                for pricelist in pricelists:
                    pricelist_id = self.env[self._name].sudo().search([('md_channel_name', '=',
                                                                        pricelist.get('channel_name'))], limit=1)
                    if not pricelist_id:
                        prepared_priceslists.append(self._prepare_pricelist_vals(pricelist, connector.company_id.id))
                    else:
                        self.env['product.pricelist.item'].sudo().action_poll_pricelist_items(pricelist_id, connector)

                if prepared_priceslists:
                    pricelist_ids = self.create(prepared_priceslists)
                    for pricelist in pricelist_ids:
                        self.env['product.pricelist.item'].sudo().action_poll_pricelist_items(pricelist, connector)

    def _prepare_pricelist_vals(self, pricelist, company_id):
        name = pricelist.get('channel_name')
        prepared_vals = {
            'name': name,
            'company_id': company_id,
            'md_channel_name': name
        }
        return prepared_vals
