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
        for rec in self:
            if not rec['barcode']:
                if "Pickup" or "PZ" in rec.loaction_id.name:
                    rec['barcode']=self.env["ir.sequence"].next_by_code('location.pickup.barcode')
                if "Stock" or "WH" in rec.loaction_id.name:
                    rec['barcode']=self.env["ir.sequence"].next_by_code('location.stock.barcode')



