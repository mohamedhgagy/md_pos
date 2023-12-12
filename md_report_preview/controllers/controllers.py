# -*- coding: utf-8 -*-
# from odoo import http


# class MdReportPreview(http.Controller):
#     @http.route('/md_report_preview/md_report_preview', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/md_report_preview/md_report_preview/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('md_report_preview.listing', {
#             'root': '/md_report_preview/md_report_preview',
#             'objects': http.request.env['md_report_preview.md_report_preview'].search([]),
#         })

#     @http.route('/md_report_preview/md_report_preview/objects/<model("md_report_preview.md_report_preview"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('md_report_preview.object', {
#             'object': obj
#         })
