# -*- coding: utf-8 -*-
# from odoo import http


# class MdConnector(http.Controller):
#     @http.route('/md_connector/md_connector', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/md_connector/md_connector/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('md_connector.listing', {
#             'root': '/md_connector/md_connector',
#             'objects': http.request.env['md_connector.md_connector'].search([]),
#         })

#     @http.route('/md_connector/md_connector/objects/<model("md_connector.md_connector"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('md_connector.object', {
#             'object': obj
#         })
