# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    md_product_id = fields.Integer(string="MD Product ")
    brand_name = fields.Char()
    category_name = fields.Char()
    short_name = fields.Char()
    status = fields.Char()
    in_stock = fields.Float(default=0.0)
    stock_limit = fields.Float(default=0.0)
    safe_stock = fields.Float(default=0.0)
    md_vat = fields.Char()

    @property
    def endpoint_prd_info(self) -> str:
        return '/mdsa/API/Products_info.php'

    @property
    def endpoint_prd_list(self) -> str:
        return '/mdsa/API/Products_List.php'

    @api.model
    def action_poll_products(self, connector):
        response = connector._send_request(headers=connector.default_headers, endpoint=self.endpoint_prd_list)

        self._proceed_response(response, connector)

    def _proceed_response(self, response, connector):
        if response and response[0].get('isSuccess', False):
            products = response[0].get('Products List', [])
            if products:
                product_ids = []
                sku_references_list = []
                products_vals_list = []
                for prd_dict in products:
                    prd_id = int(prd_dict.get('Products ID', False)) if prd_dict.get('Products ID', False) else False
                    prd_sku_ref = prd_dict.get('SKU_refrence', False)
                    payload = {
                        "SKU_refrence": prd_sku_ref
                    }
                    product_info = connector.get_info(payload=payload, endpoint=self.endpoint_prd_info)
                    if product_info and product_info[0].get('isSuccess') and product_info[0].get('ProductsCount'):
                        product_info_list = product_info[0].get('Products_Info', {})
                        if product_info_list:
                            product_info_vals = product_info_list[0] or {}
                            if product_info_vals:
                                prepared_product_vals = self._prepare_product_vals(product_info_vals)
                                if prepared_product_vals:
                                    products_vals_list.append(prepared_product_vals)
                                    product_ids.append(prd_id)
                                    sku_references_list.append(prd_sku_ref)

                exists_product_ids = self.env[self._name].sudo().search([('default_code', 'in', sku_references_list),
                                                                         ('md_product_id', 'in', product_ids)])

                if products_vals_list:
                    if exists_product_ids:
                        products_to_create = list(filter(
                            lambda prd: prd.get('md_product_id') not in exists_product_ids.mapped('md_product_id.id'),
                            products_vals_list))
                        if products_to_create:
                            products_vals_list = products_to_create
                    self.create(products_vals_list)

    def _prepare_product_vals(self, product_info) -> dict:
        if not product_info:
            return {}
        # contracting_date = user.get('Contracting_Date', False)
        # contracting_date = "1900-01-01" if contracting_date == "0000-00-00" else contracting_date
        # TODO: assign location
        prepared_product_vals = {
            'name': product_info.get('Products_Name', ''),
            'barcode': product_info.get('BarCode', ''),
            'md_product_id': product_info.get('Products_ID', False),
            'brand_name': product_info.get('Brand_Name', ''),
            'category_name': product_info.get('Category_name', ''),
            'status': product_info.get('Status', ''),
            'in_stock': product_info.get('in_Stor', 0.0),
            # 'qty_on_hand': product_info.get('in_Stor', 0.0),
            'short_name': product_info.get('Short Name', ''),
            'stock_limit': product_info.get('Stock_limit', 0.0),
            'safe_stock': product_info.get('safe_stock', 0.0),
            'default_code': product_info.get('SKU_refrence', ''),
            'md_vat': product_info.get('Vat', ''),

        }
        return prepared_product_vals
