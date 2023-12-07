from odoo import models, fields


class pwdOperation(models.TransientModel):
    _name = "pwd.operation"
    _description = 'pwd operations'

    pwd_instance_id = fields.Many2one('pwd.connector')
    from_date = fields.Date()
    operation = fields.Selection([('sync_users', 'Import Users'),
                                  ('sync_branch', 'Import Branch'),
                                  ('sync_payment_method', 'Import Payment Methods'),
                                  ('sync_categories', 'Import Categories'),
                                  ('sync_products', 'Import Products'),
                                  ('sync_orders', 'Import Orders'),
                                  # ('sync_suppliers', 'Import Suppliers'),
                                  # ('sync_inventory_items', 'Import Inventory Items'),
                                  # ('sync_modifier_products', 'Import Modifier Product'),
                                  ('sync_purchase_order', 'Import Purchase Order'),
                                  ('sync_pricelist', 'Import Pricelists'),
                                  # ('sync_transactions', 'Import Transactions'),
                                  ], default="sync_branch", required=True)

    @property
    def md_user(self):
        return self.env['res.users'].sudo()

    @property
    def md_product(self):
        return self.env['product.template'].sudo()

    @property
    def md_pricelist(self):
        return self.env['product.pricelist'].sudo()

    def pwd_execute(self):
        pwd = self.pwd_instance_id
        if pwd and pwd.is_valid_token:
            if self.operation == 'sync_users':
                self.md_user.action_poll_res_user(pwd)
                # pwd.get_import_users()
            if self.operation == 'sync_branch':
                pwd.get_branches()
            elif self.operation == 'sync_payment_method':
                pwd.get_payment_methods()
            elif self.operation == 'sync_categories':
                pwd.get_categories_methods()
            elif self.operation == 'sync_products':
                self.md_product.action_poll_products(pwd)
            elif self.operation == 'sync_orders':
                pwd.get_orders_methods(self.from_date)
            elif self.operation == 'sync_pricelist':
                self.md_pricelist.action_poll_pricelist(connector=pwd)

            else:
                pass
        # elif self.operation == 'sync_inventory_items':
        #     pwd.get_inventory_items()
        # elif self.operation == 'sync_modifier_products':
        #     pwd.with_context({'is_modifier': True}).get_products_methods()
        # elif self.operation == 'sync_purchase_order':
        #     pwd.pwd_import_purchase_orders()
        # elif self.operation == 'sync_import_warehouse':
        #     pwd.pwd_import_warehouse()
        # elif self.operation == 'sync_transactions':
        #     pwd.pwd_import_transactions()
