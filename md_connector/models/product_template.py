# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class userConfig(models.Model):
    _inherit = "product.template"

    _sql_constraints = [('md_account_id', 'unique (md_account_id)', "MD account  should be unique")]


    Representative_Number = fields.Char(string=_('REP Number'))
    Registration = fields.Char(string=_('Registration'))
    Status = fields.Char(string=_('Status'))
    supervisor_user_id = fields.Many2one('res.users', string=_('Supervisor'))
                                      # Region = fields.Char(string=_('Region'))
    # md_account_id = fields.Integer()

    md_account_id = fields.Integer(string=_('odooo ID'))

    @property
    def company(self):
        mycomp= self.env['res.company'].sudo().search([('id','=',3)])
        return mycomp

    @api.model
    def action_poll_res_user(self):
        print("hi zaki")
        if self.company.is_valid_token:
            last_shop_id = self.search([('md_account_id', '!=', False)], order='md_account_id desc', limit=1)
            if last_shop_id:
                response = self._get_user_info(account_id=last_shop_id.md_account_id + 1)
            else:
                endpoint = '/mdsa/API/Rep_List.php'
                response = self.company._send_request(headers=self.company.default_headres, endpoint=endpoint)

            self._proceed_response(response)

    def _get_user_info(self, account_id,myconnect):
        """search for user with account_id"""
        payload = {
            "account_id": account_id
        }
        endpoint = '/mdsa/API/Rep_info.php'
        response = myconnect._send_request(payload=payload, headers=self.company.default_headres, endpoint=endpoint)
        return response

    def _get_super_user_vals(self, user) -> dict:
        if not user:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        return {
            # 'Representative_Number': user.get('Representative_Number', False),
             'Representative_Number': user.get('Supervisor_ID', False),
             'login': user.get('Supervisor_ID', False),
             'password': user.get('Supervisor_ID', False),
             'name': user.get('super_Name', False),
             'email': user.get('Supervisor_Email', False),
             'company_ids':[(6,0,[3,])],
             'company_id': 3

            # 'md_account_id': user.get('account_id', False),

        }
    def _get_user_vals(self, user, mysupervisor_id) -> dict:
        if not user:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        print("user55 ",user)
        return {
             'Representative_Number': user.get('Representative_Number', False),
             'login': user.get('Representative_Number', False),
             'password': user.get('Representative_Number', False),

                    'name': user.get('name', False),
                    # 'name': user.get('Representative_En_Name', False),
                    'Registration': user.get('Registration', False),
                    'Status': user.get('Status', False),
                    'md_account_id': user.get('md_account_id', False),
                    'supervisor_user_id': mysupervisor_id.id,
                   'company_ids': [(6, 0, [3])],
                   'company_id': 3,
        }

    def _get_partner_vals(self, user) -> dict:
        print("user88" , user)
        if not user:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        return
        {
                        'name': user.get('name', False),
                        'name_ar': user.get('name_ar', False),
                        'email': user.get('email', False),
                        'city': user.get('city', False),
                        'mobile': user.get('mobile', False),
                        'default_company_id': 3,
                        'company_id': 3,
        }


    def _preceed_create(self,user):

        supervisor_val = self._get_super_user_vals(user)
        if supervisor_val['Representative_Number']:
            mysupervisor_id = self.env['res.users'].search([('Representative_Number','=',supervisor_val['Representative_Number']),],limit=1)
            if not mysupervisor_id:
                print("supervisor_val", supervisor_val)
                mysupervisor_id= self.create(supervisor_val)

            if mysupervisor_id:
                print("my",mysupervisor_id.id)
                user_vals =  self._get_user_vals(user,mysupervisor_id)
                print("user_vals" ,user_vals)
                myuser_id = self.env['res.users'].search(
                    [('Representative_Number', '=', user_vals['Representative_Number']), ], limit=1)
                if not myuser_id:
                    myuser_id = self.create(user_vals)
                    print("my name" ,myuser_id.name)
                    print("my name" ,myuser_id.partner_id)

                if myuser_id :
                    mypartner=myuser_id.partner_id

                    if mypartner:

                        partner_vals = self._get_partner_vals(user)
                        print("partner_vals" , partner_vals)
                        if partner_vals:
                             mypartner.sudo().update(partner_vals)






    def _proceed_update(self,vals):
        pass
    def _proceed_response(self, response):
        if response and response[0].get('isSuccess', False):
            user_ids = response[0].get('Representative Number', [])
            print("user_ids",user_ids)
            print("response2", response)
            if user_ids:
                user_vals_list = []
                for myuser in user_ids:
                    account_id = myuser.get('account_id', False)
                    if account_id:
                        account_id = int(account_id)
                        user_list = self._get_user_info(account_id)
                        user_object = {}
                        if user_list and user_list[0].get('isSuccess', False):
                            user_object = user_list[0].get('Rep_info', [{}])[0]

                        user_id = self.search([('md_account_id', '=', account_id)], order='md_account_id desc', limit=1)
                        prepared_user_vals = self._prepare_user_vals(user_object)
                        print("prepared_user_vals",prepared_user_vals)
                        if user_object and not user_id:
                            user_vals_list.append(prepared_user_vals)
                        if user_object and user_id:
                            user_id._proceed_update(prepared_user_vals)

                if user_vals_list:
                    for user_val in user_vals_list:
                        self._preceed_create(user_val)
            else:
                user_info = response[0].get('Rep_info')
                if user_info:
                    prepared_user_vals = self._prepare_user_vals(user_info[0])
                    print("prepared_user_vals2", prepared_user_vals)
                    self._preceed_create(prepared_user_vals)


    def _prepare_user_vals(self, user) -> dict:
        if not user:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        return {
            'Representative_Number': user.get('Representative_Number', False),
            'name': user.get('Representative_En_Name', False),
            'name_ar': user.get('Representative_Arabic_Name', False),
            'email': user.get('Email', False),
            'city': user.get('City', False),
            'mobile': user.get('Mobile', False),
            'Registration': user.get('Registration', False),
            'Region': user.get('Region', False),
            'name': user.get('super_Name', False),
            'Supervisor_ID': user.get('Supervisor_ID', False),
            'super_Name': user.get('super_Name', False),
            'supervisor_email': user.get('Supervisor_Email', False),
            'Supercisor_Phone': user.get('Supercisor_Phone', False),
            'Status': user.get('Status', False),
            'md_account_id': user.get('account_id', False),

        }






