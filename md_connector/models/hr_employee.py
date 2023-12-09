# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    default_account_id = fields.Many2one('account.account')
    journal_id = fields.Many2one('account.journal')
    warehouse_id = fields.Many2one('stock.warehouse')

    @property
    def md_code(self):
        return self.user_id.login if self.user_id.login else self.id

    def _sync_user(self, user, employee_has_image=False):
        vals = super(HrEmployee, self)._sync_user(user, employee_has_image)
        if user and user.supervisor_user_id:
            vals.update(parent_id=user.supervisor_user_id.employee_id.id)
        return vals

    def action_automate_creation(self):
        if not self:
            return
        for emp in self:
            if not emp.default_account_id:
                emp.default_account_id = emp.action_create_bank_account()
            if not emp.journal_id:
                emp.journal_id = emp.action_create_journal()
            if not emp.warehouse_id:
                emp.warehouse_id = emp.action_create_warehouse()

    def action_create_bank_account(self):
        account = self.env['account.account'].sudo()
        account_vals = account._prepare_vals(self)
        if account_vals:
            account_id = account.create(account_vals)
            return account_id.id
        return account

    def action_create_journal(self):
        journal = self.env['account.journal'].sudo()
        journal_vals = journal._prepare_vals(self)
        if journal_vals:
            journal_id = journal.create(journal_vals)
            if journal_id:
                journal_id._refine_payment_methods()
            return journal_id.id
        return journal

    def action_create_warehouse(self):
        warehouse = self.env['stock.warehouse'].sudo()
        warehouse_vals = warehouse._prepare_vals(self)
        if warehouse_vals:
            warehouse_id = warehouse.create(warehouse_vals)
            if warehouse_id:
                warehouse_id._refine_location_name()
            return warehouse_id.id
        return warehouse
