from odoo import models, fields

class ProductCheckBox(models.Model):
    _inherit = "product.template"

    auto_purchase = fields.Boolean(string="auto purchase")

class ProductCheckBox(models.Model):
    _inherit = "product.product"

    auto_purchase = fields.Boolean(string="auto purchase")