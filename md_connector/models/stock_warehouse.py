from odoo import models, fields, api, _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    @api.model
    def _prepare_vals(self, employee) -> dict:
        if not employee:
            return {}
        return {
            'name': employee.name,
            'code': f'L{employee.md_code}',
            'company_id': employee.company_id.id
        }

    def _refine_location_name(self):
        if self.lot_stock_id and self.lot_stock_id.location_id:
            self.lot_stock_id.name = self.name

