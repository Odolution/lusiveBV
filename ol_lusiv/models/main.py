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
        var1 = []


        for i in self.order_line:
            product = self.env['product.product'].search([('id', '=', i.product_id.id)])




            if len(product.seller_ids) == 0:
                temp2 = {
                    "name": i.vendor_id.id,
                    "product_uom": 'Unit',
                    "price": 0.00,
                    "delay": 1
                }
                print(temp2, 'temp2 dic')
                product.seller_ids= [(0, 0, temp2)]
            else:
                choosen_vendor=""
                for line in product.seller_ids:
                    if line.name == i.vendor_id.name:
                        choosen_vendor=line
                    print(line.id)
                    print(line.name.name)
                    var1.append(line.id)
                    print(var1, 'seller ids')
                var2 = min(var1)
                print(var2)
                min_sup_id = self.env['product.supplierinfo'].search([('id', '=', var2)])
                print(min_sup_id.id, 'min id in seller')
                vendorinseller = self.env['product.supplierinfo'].search([('id', '=', i.vendor_id.id)])



                if choosen_vendor!="":
                    temp = {
                        "vendor": choosen_vendor.name.id,
                        "uom": choosen_vendor.product_uom.id,
                        "price_cus": choosen_vendor.price,
                        "date": choosen_vendor.delay
                    }
                    print(temp, 'temp dic')





                    print(min_sup_id.id,'SUP')
                    choosen_vendor.name= min_sup_id .id
                    choosen_vendor.product_uom= min_sup_id.product_uom
                    choosen_vendor.price = min_sup_id.price
                    choosen_vendor.delay  = min_sup_id.delay

                    print(min_sup_id)

                    min_sup_id.name=temp['vendor']
                    min_sup_id.product_uom=temp['uom']
                    min_sup_id.price=temp['price_cus']
                    min_sup_id.delay=temp['date']
                else:


                    temp3 = {
                        "name":  min_sup_id.name,
                        "product_uom":min_sup_id.product_uom,
                        "price": min_sup_id.price,
                        "delay": 1
                    }
                    print(temp3, 'temp3 dic')
                    product.seller_ids = [(0, 0, temp3)]

                    # min_sup_id = self.env['product.supplierinfo'].search([('id', '=', var2)])
                    # print(min_sup_id.id, 'SUP')
                    # line.name = min_sup_id.name.id
                    # line.product_uom = min_sup_id.product_uom
                    # line.price = min_sup_id.price
                    # line.delay = min_sup_id.delay
                    #
                    # print(min_sup_id)

                    min_sup_id.name = i.vendor_id.id
                    min_sup_id.product_uom =  i.product_uom.id,
                    # min_sup_id.price = ,
                    min_sup_id.delay =1
                #     line.seller_ids = [(0, 0,  {
                #         "name": line.name,
                #         "product_uom": line.product_uom,
                #         "price": line.price,
                #         # "delay": line.delay
                #
                # })]











        # print('Seller Name',line.name.name)

        # elif line.name != i.vendor_id.name:
        #     temp2 = {
        #         "vendor": i.vendor_id.id,
        #         "uom": 'Unit',
        #         "price_cus": 0.00,
        #         "date":1
        #     }
        #     print(temp2, 'temp2 dic')
        #     # min_sup_id = self.env['product.supplierinfo'].search([('id', '=', var2)])
        #     print(min_sup_id.id, 'SUP')
        #     line.name = min_sup_id.name.id
        #     line.product_uom = min_sup_id.product_uom
        #     line.price = min_sup_id.price
        #     line.delay = min_sup_id.delay
        #     # sup = dict(temp)
        #     print(min_sup_id)
        #
        #     min_sup_id.name = temp2['vendor']
        #     min_sup_id.product_uom = temp2['uom']
        #     min_sup_id.price = temp2['price_cus']
        #     min_sup_id.delay = temp2['date']

        return super(Inheritssaleorder, self).action_confirm()
