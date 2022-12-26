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

    @api.onchange("product_template_id")
    def select_default_vendor(self):
        for rec in self:
            if rec.product_template_id and rec.product_template_id.seller_ids:
                rec.vendor_id = rec.product_template_id.seller_ids[0].name.id
                rec.leadtime = rec.product_template_id.seller_ids[0].delay





class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    url_pr = fields.Char('Url')
    lead_time = fields.Char('Lead_Time')



    def _compute_valuefrom_saleline(self):
        # pol = self.order_id


        for line in self:
            so = line.order_id._get_sale_orders().ids
            sol=None
            if len(so)==1:
                sol = self.env["sale.order.line"].search(
                    [("order_id", '=',so ), ("product_id", "=", line.product_id.id)])

            elif len(so)>0:
                so = max(so)
                sol = self.env["sale.order.line"].search(
                    [("order_id", '=',so ), ("product_id", "=", line.product_id.id)])
            if sol:
                for sline in sol:

                    line.url_pr = sline.url
                    line.lead_time = sline.leadtime






