# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class md_report_preview(models.Model):
#     _name = 'md_report_preview.md_report_preview'
#     _description = 'md_report_preview.md_report_preview'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
