# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _sync_user(self, user, employee_has_image=False):
        vals = super(HrEmployee, self)._sync_user(user, employee_has_image)
        if user and user.supervisor_user_id:
            vals.update(parent_id=user.supervisor_user_id.employee_id.id)
        return vals

    @api.model
    def action_automate_creation(self):
        if not self:
            return
        for emp in self:
            income_account_id = emp.action_create_income_account()
            journal_id = emp.action_create_journal()
            warehouse_id = emp.action_create_warehouse()

    def action_create_income_account(self):
        account = self.env['account_account'].sudo()
        account_vals = account._prepare_vals(self)
        if account_vals:
            account_id = account.create(account_vals)
            return account_id
        return account

    def action_create_journal(self):
        journal = self.env['account.journal'].sudo()
        journal_vals = journal._prepare_vals(self)
        if journal_vals:
            journal_id = journal.create(journal_vals)
            return journal_id
        return journal

    def action_create_warehouse(self):
        warehouse = self.env['stock.warehouse'].sudo()
        warehouse_vals = warehouse._prepare_vals(self)
        if warehouse_vals:
            warehouse_id = warehouse.create(warehouse_vals)
            return warehouse_id
        return warehouse
