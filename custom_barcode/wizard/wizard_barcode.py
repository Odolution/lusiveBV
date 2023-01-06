
from collections import defaultdict
from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'
    active_model=fields.Char(string="Active Model")
    def _prepare_data(self,active_model,ids):
        recs=self.env[active_model].search([('id', 'in',ids)])
        return recs
    def process(self):
        self.print_format='dymo'
        xml_id="custom_barcode.report_print_custom_product_barcode"

        self.active_model = ''
        if self.product_tmpl_ids:
            products = self.product_tmpl_ids.ids
            self.active_model = 'product.template'
        elif self.product_ids:
            products = self.product_ids.ids
            self.active_model = 'product.product'
        else:
            raise UserError(_("No product to print, if the product is archived please unarchive it before printing its label."))

        # Build data to pass to the report
        data = {
            'active_model': self.active_model,
            'quantity_by_product': {p: self.custom_quantity for p in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
            'docs':self,
            'ids':[product.id for product in self.product_ids] if self.product_ids else [product.id for product in self.product_tmpl_ids],
            "custom_quantity":self.custom_quantity
        }
        # vals=_prepare_data(self.env,data)
        # raise UserError(str(data))
        
        report_action = self.env.ref(xml_id).report_action(self, data=data)
        report_action.update({'close_on_report_download': True,
                                
                                })
        
        return report_action
