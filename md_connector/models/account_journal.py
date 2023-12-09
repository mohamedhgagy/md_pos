# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def _prepare_vals(self, employee) -> dict:
        if not employee:
            return {}
        return {

        }
