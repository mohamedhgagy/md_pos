# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class md_connector(models.Model):
#     _name = 'md_connector.md_connector'
#     _description = 'md_connector.md_connector'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
