from odoo import models, fields, api, _

class Inheritssaleorder(models.Model):
    _inherit = 'sale.order'

    purchase_price = fields.Integer(string='Purchase Price', compute="_compute_purchase_price")

    def _compute_purchase_price(self):
        pass