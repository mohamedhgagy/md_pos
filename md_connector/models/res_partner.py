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
    supervisor_id = fields.Char(string='Supervisor ID')
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
    def company(self):
        return self.env.company

    @api.model
    def action_poll_pos(self):
        if self.company.is_valid_token:
            last_shop_id = self.search([('md_account_id', '!=', False)], order='md_account_id desc', limit=1)
            if last_shop_id:
                response = self._get_pos_info(account_id=last_shop_id.md_account_id + 1)
            else:
                endpoint = '/mdsa/API/POS_LIST.php'
                response = self.company._send_request(headers=self.company.default_headers, endpoint=endpoint)
            self._proceed_response(response)

    def _get_pos_info(self, account_id):
        """search for pos with account_id"""
        payload = {
            "account_id": account_id
        }
        endpoint = '/mdsa/API/POS_info.php'
        response = self.company._send_request(payload=payload, headers=self.company.default_headers, endpoint=endpoint)
        return response

    def _proceed_response(self, response):
        if response and response[0].get('isSuccess', False):
            pos_ids = response[0].get('POSIDs', [])
            if pos_ids:
                pos_vals_list = []
                for pos in pos_ids:
                    account_id = pos.get('account_id', False)
                    if account_id:
                        account_id = int(account_id)
                        pos_list = self._get_pos_info(account_id)
                        pos_object = {}
                        if pos_list and pos_list[0].get('isSuccess', False):
                            pos_object = pos_list[0].get('POS_info', [{}])[0]

                        pos_id = self.search([('md_account_id', '=', account_id)], order='md_account_id desc', limit=1)
                        prepared_pos_vals = self._prepare_pos_vals(pos_object)
                        if pos_object and not pos_id:
                            pos_vals_list.append(prepared_pos_vals)
                        if pos_object and pos_id:
                            pos_id.update(prepared_pos_vals)

                if pos_vals_list:
                    for pos_val in pos_vals_list:
                        self.create(pos_val)
            else:
                pos_info = response[0].get('POS_info')
                if pos_info:
                    prepared_pos_vals = self._prepare_pos_vals(pos_info[0])
                    self.create(prepared_pos_vals)

    def _prepare_pos_vals(self, pos) -> dict:
        if not pos:
            return {}
        contracting_date = pos.get('Contracting_Date', False)
        contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        return {
            'md_pos_id': pos.get('POS_ID', False),
            'name': pos.get('Name_En', False),
            'name_ar': pos.get('Name_AR', False),
            'md_account_id': pos.get('account_id', False),
            'city': pos.get('City', False),
            'district': pos.get('Region', False),
            'region': pos.get('district', False),
            'owner_name': pos.get('owner_name', False),
            'manager_name': pos.get('Manager_Name', False),
            'super_name': pos.get('super_Name', False),
            'supervisor_id': pos.get('Supervisor_ID', False),
            'supervisor_email': pos.get('Supervisor_Email', False),
            'supercisor_phone': pos.get('Supercisor_Phone', False),
            'rep_name': pos.get('Rep_Name', False),
            'rep_id': pos.get('Rep_ID', False),
            'special_access_group': pos.get('Special_Access_Group', False),
            'pos_phone': pos.get('POS_Phone', False),
            'contracting_date': contracting_date,
            'license_cr': pos.get('License/CR', False),
            'registration': pos.get('Registration', False),
            'channel_name': pos.get('Channel_Name', False),
            'pool_name': pos.get('POOL_Name', False),
            'status': pos.get('Status', False),

        }

    def _get_partner_vals(self, user_vals) -> dict:
        print("user88", user_vals)
        if not user_vals:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        partner_vals = {
            'name': user_vals.get('name', False),
            'name_ar': user_vals.get('name_ar', False),
            'email': user_vals.get('email', False),
            'city': user_vals.get('city', False),
            'mobile': user_vals.get('mobile', False),
            # 'default_company_id': user_vals.get('company_id', False),
            'company_id': user_vals.get('company_id', False),
        }
        return partner_vals
