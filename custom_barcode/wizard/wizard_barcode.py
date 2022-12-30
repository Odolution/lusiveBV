from odoo import api, fields, models

# class ProductLabelLayout(models.TransientModel):
#     _inherit = 'product.label.layout'
#     _description = 'Choose the sheet layout to print the labels'

#     print_format = fields.Selection([
#         ('dymo', 'Dymo'),
#         ], string="Format", default='dymo', required=True)

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'
    def process(self):
        self.print_format='dymo'
        res=super(ProductLabelLayout,self).process()
        return res

