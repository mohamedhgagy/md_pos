from odoo import models, fields, api, _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    @api.model
    def _prepare_vals(self, employee) -> dict:
        if not employee:
            return {}
        return {
            'name': employee.name,
            'code': employee.code if employee.code else employee.id,
            'company_id': employee.company_id.id
        }
