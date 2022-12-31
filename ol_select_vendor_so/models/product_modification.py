from odoo import models, fields,api

class ProductCheckBox(models.Model):
    _inherit = "product.template"

    auto_purchase = fields.Boolean(string="Auto Purchase")
    allow_all_vendors = fields.Boolean(string='Allow All Vendors')

    # @api.onchange('auto_purchase')
    # def onchance_auto_purchase(self):
    #     for product in self.product_variant_id:
    #         product.auto_purchase = self.auto_purchase


class ProductCheckBox(models.Model):
    _inherit = "product.product"

    auto_purchase = fields.Boolean(string="auto purchase")