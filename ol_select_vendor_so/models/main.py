from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import base64
import requests
import datetime
from odoo.exceptions import ValidationError


class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vendor_id = fields.Many2one(comodel_name='res.partner',
                                string="Vendor")

    url = fields.Char(stirng='URl')


class Inheritssaleorder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):



        for i in self.order_line:

            product = self.env['product.product'].search([('id', '=', i.product_id.id)])

            temp = []
            for j in product.seller_ids:
                temp.append(j.name.name)

            if i.vendor_id.name not in temp:
                temp2 = {
                    "name": i.vendor_id.id,
                    "product_uom": 'Unit',
                    "price": 0.00,
                    "delay": 1,
                    "sequence": 1
                }
                product.seller_ids = [(0, 0, temp2)]

                temp.append(i.vendor_id.name)

            for j in product.seller_ids:
                if j.name.name == i.vendor_id.name:
                    j.sequence = 1
                else:
                    j.sequence += 1




        return super(Inheritssaleorder, self).action_confirm()
