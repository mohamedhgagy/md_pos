# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResUser(models.Model):
    _inherit = "res.users"

    _sql_constraints = [('md_account_id', 'unique (md_account_id)', "MD account  should be unique")]

    Representative_Number = fields.Char(string=_('REP Number'))
    Registration = fields.Char(string=_('Registration'))
    Status = fields.Char(string=_('Status'))
    supervisor_user_id = fields.Many2one('res.users', string=_('Supervisor'))
    # Region = fields.Char(string=_('Region'))
    # md_account_id = fields.Integer()

    md_account_id = fields.Integer(string=_('odoo ID'))

    @property
    def company(self):
        mycomp = self.env['res.company'].sudo().search([('id', '=', 3)])
        return mycomp

    @api.model
    def action_poll_res_user(self, connector):
        if connector and connector.is_valid_token:
            last_user_id = self.search([('md_account_id', '!=', False)], order='md_account_id desc', limit=1)
            if last_user_id:
                response = self._get_user_info(account_id=last_user_id.md_account_id + 1)
            else:
                endpoint = '/mdsa/API/Rep_List.php'
                response = connector._send_request(headers=connector.default_headers, endpoint=endpoint)

            self._proceed_response(response, connector)

    def _get_user_info(self, account_id, connector):
        """search for user with account_id"""
        payload = {
            "account_id": account_id
        }
        endpoint = '/mdsa/API/Rep_info.php'
        response = connector._send_request(payload=payload, headers=connector.default_headers, endpoint=endpoint)
        return response

    def _get_super_user_vals(self, user_obj, connector) -> dict:
        if not user_obj:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        return {
            # 'Representative_Number': user.get('Representative_Number', False),
            'Representative_Number': user_obj.get('Supervisor_ID', False),
            'login': user_obj.get('Supervisor_ID', False),
            'password': user_obj.get('Supervisor_ID', False),
            'name': user_obj.get('super_Name', False),
            'email': user_obj.get('Supervisor_Email', False),
            'company_ids': [(6, 0, connector.company_id.ids)],
            'company_id': connector.company_id.id

            # 'md_account_id': user.get('account_id', False),

        }

    def _get_base_user_vals(self, user_vals, mysupervisor_id) -> dict:
        if not user_vals:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        print("user55 ", user_vals)
        return {
            'Representative_Number': user_vals.get('Representative_Number', False),
            'login': user_vals.get('Representative_Number', False),
            'password': user_vals.get('Representative_Number', False),

            'name': user_vals.get('name', False),
            # 'name': user.get('Representative_En_Name', False),
            'Registration': user_vals.get('Registration', False),
            'Status': user_vals.get('Status', False),
            'md_account_id': user_vals.get('md_account_id', False),
            'supervisor_user_id': mysupervisor_id.id,
            'company_ids': [(6, 0, mysupervisor_id.company_ids.ids)],
            'company_id': mysupervisor_id.company_id.id,
        }

    def _preceed_create(self, user_vals, connector):

        supervisor_val = self._get_super_user_vals(user_vals, connector)
        if supervisor_val['Representative_Number']:
            mysupervisor_id = self.search(
                [('Representative_Number', '=', supervisor_val['Representative_Number']), ], limit=1)
            if not mysupervisor_id:
                print("supervisor_val", supervisor_val)
                mysupervisor_id = self.create(supervisor_val)

            if mysupervisor_id:
                print("my", mysupervisor_id.id)
                user_base_vals = self._get_base_user_vals(user_vals, mysupervisor_id)
                print("user_vals", user_base_vals)
                myuser_id = self.env['res.users'].search(
                    [('Representative_Number', '=', user_base_vals['Representative_Number']), ], limit=1)
                if not myuser_id:
                    myuser_id = self.create(user_base_vals)
                    print("my name", myuser_id.name)
                    print("my name", myuser_id.partner_id)

                if myuser_id:
                    mypartner = myuser_id.partner_id

                    if mypartner:

                        partner_vals = mypartner._get_partner_vals(user_vals)
                        print("partner_vals", partner_vals)
                        if partner_vals:
                            mypartner.sudo().update(partner_vals)

    def _proceed_update(self, vals):
        pass

    def _proceed_response(self, response, connector):
        if response and response[0].get('isSuccess', False):
            user_ids = response[0].get('Representative Number', [])
            if user_ids:
                user_vals_list = []
                for myuser in user_ids:
                    account_id = myuser.get('account_id', False)
                    if account_id:
                        account_id = int(account_id)
                        user_list = self._get_user_info(account_id, connector)
                        user_object = {}
                        if user_list and user_list[0].get('isSuccess', False):
                            user_object = user_list[0].get('Rep_info', [{}])[0]

                        user_id = self.search([('md_account_id', '=', account_id)], order='md_account_id desc', limit=1)
                        prepared_user_vals = self._prepare_user_vals(user_object, company=connector.company_id.id)
                        print("prepared_user_vals", prepared_user_vals)
                        if user_object and not user_id:
                            user_vals_list.append(prepared_user_vals)
                        if user_object and user_id:
                            user_id._proceed_update(prepared_user_vals)

                if user_vals_list:
                    for user_val in user_vals_list:
                        self._preceed_create(user_val, connector)
            else:
                user_info = response[0].get('Rep_info')
                if user_info:
                    prepared_user_vals = self._prepare_user_vals(user_info[0], company=connector.company_id.id)
                    print("prepared_user_vals2", prepared_user_vals)
                    self._preceed_create(prepared_user_vals, connector)

    def _prepare_user_vals(self, user_vals, company) -> dict:
        if not user_vals:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        return {
            'Representative_Number': user_vals.get('Representative_Number', False),
            'name': user_vals.get('Representative_En_Name', False),
            'name_ar': user_vals.get('Representative_Arabic_Name', False),
            'email': user_vals.get('Email', False),
            'city': user_vals.get('City', False),
            'mobile': user_vals.get('Mobile', False),
            'Registration': user_vals.get('Registration', False),
            'Region': user_vals.get('Region', False),
            # 'name': user.get('super_Name', False),
            'Supervisor_ID': user_vals.get('Supervisor_ID', False),
            'super_Name': user_vals.get('super_Name', False),
            'supervisor_email': user_vals.get('Supervisor_Email', False),
            'Supercisor_Phone': user_vals.get('Supercisor_Phone', False),
            'Status': user_vals.get('Status', False),
            'md_account_id': user_vals.get('account_id', False),
            'company_ids': [(6, 0, [company, ])],
            'company_id': company

        }
