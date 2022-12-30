from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import base64
import requests
import datetime
from odoo.exceptions import ValidationError


class InheritPurchaseOrder(models.Model):
    _inherit='purchase.order'
    SO_id = fields.Many2one("sale.order")


class Inheritssaleorder(models.Model):
    _inherit = 'sale.order'

    PO_ids = fields.One2many('purchase.order','SO_id')
    pos_count = fields.Integer("Purchase Order Count",compute='_compute_purchase_order')

    def _compute_purchase_order(self):
        self.pos_count = len(self.PO_ids)

    def action_confirm(self):
        # raise UserError(str("Custom Purchase Order Method is being called"))
 
        # for i in self.order_line:

        #     product = self.env['product.product'].search([('id', '=', i.product_id.id)])


        #     temp = []
        #     for j in product.seller_ids:
        #         temp.append(j.name.name)

        #     if i.vendor_id and i.vendor_id.name not in temp:
        #         temp2 = {
        #             "name": i.vendor_id.id,
        #             "product_uom": 'Unit',
        #             "price": 0.00,
        #             "delay": 1,
        #             "sequence": 1
        #         }
        #         product.seller_ids = [(0, 0, temp2)]

        #         temp.append(i.vendor_id.name)

        #     for j in product.seller_ids:
        #         if j.name.name == i.vendor_id.name:
        #             j.sequence = 1
        #         else:
        #             j.sequence += 1


        # Custom Purchase Order
        for rec in self:
            unique_vendors = []
            vendorPOdict={}
            for i in rec.order_line:
                if i.vendor_id not in unique_vendors and i.product_id.auto_purchase:
                    unique_vendors.append(i.vendor_id)
            for vendor in unique_vendors:
                data2={}
                data2['partner_id']= vendor.id
                data2['SO_id']=self.id
                po = self.env['purchase.order'].create(data2)
                vendorPOdict[vendor]=po

            data={}

            for line in rec.order_line:
                
                if line.product_id.auto_purchase:
                    raise UserError(line.product_id.auto_purchase)
                    po=vendorPOdict[line.vendor_id]
                    data['url_pr'] = line.url
                    data['item_price'] = line.item_price
                    data['lead_time'] = line.leadtime
                    data['product_id'] = line.product_id.id
                    data['name'] = line.name
                    data['product_qty'] = line.product_uom_qty
                    data['price_unit'] = line.price_unit
                    data['order_id']=po.id
            
                    pol=self.env['purchase.order.line'].create(data)
            raise UserError(str(data))
        

        # res=super(Inheritssaleorder, self).action_confirm()
        # return res


    def purchase_icon_show(self):
        for rec in self:
            purchase_orders = [i.id for i in rec.PO_ids]
            if len(purchase_orders) > 1:
                return {
                    'name': 'Purchase Order',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'purchase.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'domain': [('id', 'in', purchase_orders)],
                    

                }
            if len(purchase_orders) == 1:
                return {
                    'name': 'Purchase Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'purchase.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'res_id': purchase_orders[0],
                }
        



        





