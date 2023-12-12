# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class PreviewInvoiceController(http.Controller):

    @http.route('/api/mdsa/preview/invoice/<model("account.move"):invoice>', type='json', auth='user')
    def preview_invoice(self, invoice, **kwargs):
        # Fetch the invoice based on the provided ID
        if invoice:
            # Generate the URL to preview the invoice
            preview_url = invoice.get_portal_url()

            # Construct JSON response
            response = {
                'invoice_id': invoice.id,
                'preview_url': preview_url,
            }

            return response, 200

        return {'error': 'Invoice not found'}, 404

    @http.route('/api/mdsa/get/invoice/<model("sale.order"):sale_order>', type='json', auth='user')
    def get_invoice(self, sale_order, **kwargs):
        if sale_order.sudo().invoice_ids:
            invoice_urls = [self.preview_invoice(inv) for inv in sale_order.invoice_ids]
            return invoice_urls
        return {'error': 'Invoices not found'}, 404
