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

    url = fields.Char(string='URl')
    leadtime = fields.Char(string='Lead Time')
    item_price = fields.Float(string='Item Price')
    

    @api.onchange("product_template_id")
    def select_default_vendor(self):
        for rec in self:
            if rec.product_template_id and rec.product_template_id.seller_ids:
                rec.vendor_id = rec.product_template_id.seller_ids[0].name.id
                rec.leadtime = rec.product_template_id.seller_ids[0].delay
        if not self.product_template_id or self.product_template_id.id == 5:
            return {'domain': {'vendor_id': []}}
        this_vendors=[]
        for line in self.product_template_id.seller_ids:
            this_vendors.append(line.name.id)
        return {'domain': {'vendor_id': [('id', 'in', this_vendors)]}}




class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    url_pr = fields.Char(string='Url')
    lead_time = fields.Char(string='Lead_Time')
    item_price = fields.Float(string='Item Price')

    


    #     for line in self:
    #         so = line.order_id._get_sale_orders().ids
    #         sol=None
    #         if len(so)==1:
    #             sol = self.env["sale.order.line"].search(
    #                 [("order_id", '=',so ), ("product_id", "=", line.product_id.id)])

    #         elif len(so)>0:
    #             so = max(so)
    #             sol = self.env["sale.order.line"].search(
    #                 [("order_id", '=',so ), ("product_id", "=", line.product_id.id)])
    #         if sol:
    #             for sline in sol:
    #                 line.url_pr = sline.url if sline.url != "" else ""                    
    #                 line.item_price = sline.item_price if sline.item_price != float(0) else 0
    #                 line.lead_time = sline.leadtime if sline.leadtime != "" else ""
                    

         




