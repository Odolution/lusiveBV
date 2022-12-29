from odoo import api, fields, models
from odoo.exceptions import UserError

class producttmpl_location(models.Model):
    _inherit = 'product.template'

    put_away_location=fields.Many2one('stock.location' ,'Put Away Location' , compute = "compute_location")
    
    # product=fields.Many2one('stock.location' ,'Location', related='product_tmpl_id.product_id')
    # location=fields.Many2one('stock.location' ,'Location', related='product_tmpl_id.location_out_id')

    def compute_location(self):
        for rec in self:
            products=self.env["product.product"].search([("product_tmpl_id","=",rec.id)])
            if products:
                putaways=self.env["stock.putaway.rule"].search([("product_id",'=',products[0].id)])
                if putaways:
                    rec.put_away_location=putaways[0].location_out_id.id
class productprd_location(models.Model):
    _inherit = 'product.product'

    put_away_location=fields.Many2one('stock.location' ,'Put Away Location' , compute = "compute_location")
    
    # product=fields.Many2one('stock.location' ,'Location', related='product_tmpl_id.product_id')
    # location=fields.Many2one('stock.location' ,'Location', related='product_tmpl_id.location_out_id')

    def compute_location(self):
        for rec in self:
            putaways=self.env["stock.putaway.rule"].search([("product_id",'=',rec.id)])
            if putaways:
                raise UserError(putaways[0].location_out_id.id)
                rec.put_away_location=putaways[0].location_out_id.id
