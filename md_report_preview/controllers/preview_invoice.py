# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

import json
class PreviewInvoiceController(http.Controller):

    @http.route('/api/mdsa/preview/invoice/<model("account.move"):invoice>', type='json', auth='user')
    def preview_invoice(self, invoice, **kwargs):
        # Fetch the invoice based on the provided ID
        if invoice:
            # Generate the URL to preview the invoice
            preview_url = invoice.get_portal_url()
            host_url = request.httprequest.host_url[:-1] if request.httprequest.host_url else ''
            # Construct JSON response
            response = {
                'invoice_id': invoice.id,
                'preview_url': host_url+preview_url,
            }

            return response, 200

        return {'error': 'Invoice not found'}, 404

    @http.route('/api/mdsa/get/invoices', type='json', auth='user', method=['POST'])
    def get_invoice(self):
        error = {'error': 'Invoices not found'}, 404
        order_dict = json.loads(request.httprequest.data)
        order_name = order_dict.get('order_name', False)
        if order_name:
            sale_order = request.env['sale.order'].sudo().search([('name', '=', order_name)], limit=1)
            if sale_order and sale_order.sudo().invoice_ids:
                invoice_urls = [self.preview_invoice(inv)[0] for inv in sale_order.invoice_ids]
                return invoice_urls, 200
            return error, 400
        return error, 400
