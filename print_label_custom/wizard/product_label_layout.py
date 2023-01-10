
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError




class LabelReportWizard(models.TransientModel):
    _name="label.report.wizard"
    _description='Label receivable Wizard'

    custom_quantity = fields.Integer('Quantity', default=1, required=True)
    product_ids = fields.Many2many('product.product')
    product_tmpl_ids = fields.Many2many('product.template')
    active_model=fields.Char(string="Active Model")
    

    def _prepare_data(self,active_model,ids):
        recs=self.env[active_model].search([('id', 'in',ids)])
        return recs
    def process(self):
        line_ids = self.env.context.get('active_ids', [])
        line_rec = self.env['stock.picking'].browse(line_ids)
    
        move_line_data=self.env["stock.picking"].search([('id', '=',line_rec.id)])
     
        
        xml_id="custom_print_label.report_print_custom_print_label"
# 
        self.active_model = 'stock.move.line'
      
        data = {
            'active_model': self.active_model,
            'docs':move_line_data,
            'ids':[line.id for line in move_line_data.move_line_ids_without_package] ,
            "custom_quantity":self.custom_quantity
        }
   
        
        report_action = self.env.ref("print_label_custom.report_print_custom_print_label").report_action(self, data=data)
        report_action.update({'close_on_report_download': True,
                                
                                })
        
        return report_action

    
    