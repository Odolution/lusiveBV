from odoo import api, fields, models
from odoo.exceptions import UserError

class inheritStockPicking(models.Model):
    _inherit = 'stock.picking'



    def custom_print_label(self):
        view = self.env.ref('print_label_custom.print_label_custom_layout_form')
        return {
            'name': ('Choose Labels Layout'),
            'type': 'ir.actions.act_window',
            'res_model':'label.report.wizard',
            'views': [(view.id, 'form')],
            'target': 'new',
            'context': {
                'default_product_ids': self.move_lines.product_id.ids,
                'default_move_line_ids': self.move_line_ids.ids,
                'default_picking_quantity': 'picking'},
        }

class inheritStockPicking(models.Model):
    _inherit = 'stock.location'

   
    def generate_barcode(self):
       
        if not self['barcode']:
            if self.location_id:
                if self.location_id.name=="Pickup" or "PZ" in self.location_id.name:
                    self['barcode']=self.env["ir.sequence"].next_by_code('location.pickup.barcode')
                elif self.location_id.name=="Stock" or "WH" in self.location_id.name:
                    self['barcode']=self.env["ir.sequence"].next_by_code('location.stock.barcode')



