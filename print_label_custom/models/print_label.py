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
