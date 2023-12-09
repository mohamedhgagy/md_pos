# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.model
    def _prepare_vals(self, employee, **kwargs) -> dict:
        if not employee:
            return {}
        return {
            'code': employee.md_code,
            'name': employee.name,
            'account_type': 'asset_cash',
            'company_id': employee.company_id.id,
            'currency_id': employee.company_id.currency_id.id,
            'reconcile': True
        }
