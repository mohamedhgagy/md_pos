# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    _sql_constraints = [('md_account_id', 'unique (md_account_id)', "MD account  should be unique")]

    md_pos_id = fields.Char()
    name_ar = fields.Char(string='Name (Arabic)')
    # city = fields.Char(string='City')
    region = fields.Char(string='Region')
    # district = fields.Char(string='District')
    langitute = fields.Char(string='Langitute')
    latitude = fields.Char(string='Latitude')
    owner_name = fields.Char(string='Owner Name')
    manager_name = fields.Char(string='Manager Name')
    super_name = fields.Char(string='Super Name')
    supervisor_id = fields.Many2one('res.users')
    supervisor_email = fields.Char(string='Supervisor Email')
    supercisor_phone = fields.Char(string='Supervisor Phone')
    rep_name = fields.Char(string='Representative Name')
    rep_id = fields.Char(string='Representative ID')
    special_access_group = fields.Char(string='Special Access Group')
    pos_phone = fields.Char(string='POS Phone')
    contracting_date = fields.Date(string='Contracting Date')
    license_cr = fields.Char(string='License/CR')
    channel_name = fields.Char(string='Channel Name')
    pool_name = fields.Char(string='POOL Name')
    registration = fields.Char()
    status = fields.Char()
    district = fields.Char(string='District')
    md_account_id = fields.Integer()

    @property
    def endpoint_pos_lst(self):
        return '/mdsa/API/POS_LIST.php'

    @property
    def end_point_pos_info(self):
        return '/mdsa/API/POS_info.php'

    @api.model
    def action_poll_pos(self, connector):
        response = connector._send_request(headers=connector.default_headers,
                                           endpoint=self.endpoint_pos_lst)
        self._proceed_response(response, connector)

    def _get_pos_info(self, account_id, connector):
        """search for pos with account_id"""
        payload = {
            "account_id": account_id
        }
        response = connector._send_request(payload=payload, headers=connector.default_headers,
                                           endpoint=self.end_point_pos_info)
        return response

    def _proceed_response(self, response, connector):
        if response and response[0].get('isSuccess', False):
            pos_ids = response[0].get('POSIDs', [])
            if pos_ids:
                pos_vals_list = []
                for pos in pos_ids:
                    account_id = pos.get('account_id', False)
                    if account_id:
                        account_id = int(account_id)
                        pos_list = self._get_pos_info(account_id, connector)
                        pos_object = {}
                        if pos_list and pos_list[0].get('isSuccess', False):
                            pos_object = pos_list[0].get('POS_info', [{}])[0]

                        pos_id = self.search([('md_account_id', '=', account_id)], order='md_account_id desc', limit=1)
                        prepared_pos_vals = self._prepare_pos_vals(pos_object, connector.company_id)
                        if pos_object and not pos_id:
                            pos_vals_list.append(prepared_pos_vals)
                        if pos_object and pos_id:
                            pos_id.update(prepared_pos_vals)

                if pos_vals_list:
                    for pos_val in pos_vals_list:
                        self.create(pos_val)

    def _prepare_pos_vals(self, pos, company) -> dict:
        if not pos:
            return {}
        contracting_date = pos.get('Contracting_Date', False)
        contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date

        # TODO: assign location
        pos_vals = {
            'company_type': 'company',
            'md_pos_id': pos.get('POS_ID', False),
            'name': pos.get('Name_En', False),
            'name_ar': pos.get('Name_AR', False),
            'md_account_id': pos.get('account_id', False),
            'city': pos.get('City', False),
            'district': pos.get('Region', False),
            'street2': pos.get('Region', False),
            'region': pos.get('district', False),
            'street': pos.get('district', False),
            'owner_name': pos.get('owner_name', False),
            'manager_name': pos.get('Manager_Name', False),
            'super_name': pos.get('super_Name', False),
            'supervisor_email': pos.get('Supervisor_Email', False),
            'supercisor_phone': pos.get('Supercisor_Phone', False),
            'rep_name': pos.get('Rep_Name', False),
            'rep_id': pos.get('Rep_ID', False),
            'special_access_group': pos.get('Special_Access_Group', False),
            'phone': pos.get('POS_Phone', False),
            'contracting_date': contracting_date,
            'license_cr': pos.get('License/CR', False),
            'registration': pos.get('Registration', False),
            'channel_name': pos.get('Channel_Name', False),
            'pool_name': pos.get('POOL_Name', False),
            'status': pos.get('Status', False),
            'company_id': company.id

        }
        user_rep_number = pos.get('Rep_ID', False)
        if user_rep_number:
            user_id = self.env['res.users'].sudo().search([('Representative_Number', '=', user_rep_number)], limit=1)
            pos_vals.update(user_id=user_id.id, supervisor_id=user_id.supervisor_user_id.id)
        pricelist_name = pos.get('Channel_Name', False)
        if pricelist_name:
            pricelist_id = self.env['product.pricelist'].sudo().search([('md_channel_name', '=', pricelist_name)],
                                                                       limit=1)
            if pricelist_id:
                pos_vals.update(property_product_pricelist=pricelist_id.id)
        return pos_vals
