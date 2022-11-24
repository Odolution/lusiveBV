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
    leadtime = fields.Char(stirng='Lead Time')






class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    url_pr = fields.Char('Url', compute='_compute_valuefrom_saleline')
    lead_time = fields.Char('Lead_Time',compute='_compute_valuefrom_saleline')



    def _compute_valuefrom_saleline(self):
        # pol = self.order_id
        so=self.order_id._get_sale_orders().ids


        for line in self:

            sol = self.env["sale.order.line"].search(
                [("order_id", '=',so ), ("product_id", "=", line.product_id.id)])

            for sline in sol:

                line.url_pr = sline.url
                line.lead_time = sline.leadtime






