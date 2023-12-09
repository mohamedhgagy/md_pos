# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def _prepare_vals(self, employee) -> dict:
        if not employee:
            return {}
        return {
            'name': employee.name,
            'type': 'bank',
            'default_account_id': employee.bank_account_id.id,
            'code': f'P{employee.md_code}',
            'currency_id': employee.company_id.currency_id.id
        }

    def _refine_payment_methods(self):
        """set default_account_id for incoming and outgoing payment read from default_account_id """
        if self.inbound_payment_method_line_ids:
            self.inbound_payment_method_line_ids[0].payment_account_id = self.default_account_id.id
        if self.outbound_payment_method_line_ids:
            self.outbound_payment_method_line_ids[0].payment_account_id = self.default_account_id.id
        # inbound_payment_method_line_ids = incoming payments
        # outbound_payment_method_line_ids = outgoing payments

