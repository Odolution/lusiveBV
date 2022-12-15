from odoo import api, fields, models
from odoo.exceptions import UserError
class crm(models.Model):
    _inherit='crm.lead'

    availability= fields.Datetime(string = 'Customer Availability')
    with_whom= fields.Char(string = 'With Whom')
    how_long= fields.Char(string = 'How Long')
    alone_or_two= fields.Char(string = 'Alone Or With 2')
    contact_person= fields.Char(string = 'Contact Person')
    todos= fields.Html(string = 'Todos')
    location_material= fields.Text(string = 'Location And Material')
    extra_information= fields.Html(string = 'Extra Information')
    material_and_tools_ids= fields.Many2many('product.product', string='Material and Tools')
    # consumable_ids= fields.Many2many('product.product', string='Consumable')
    consumable_ids = fields.Many2many('product.product', 'product_product_costum')


    resource_ids=fields.One2many('user.resources','crm_id',string='Resource_Id')
    
    # @api.onchange('partner_id')
    # def item_delivered_ids_onchange(self):
        
    #     domain={'domain': {'material_and_tools_ids': [('detailed_type', '=', 'product')]}}
    #     raise UserError(str(domain))
    #     return domain

    # @api.onchange('partner_id')
    # def item_delivered_ids_onchange(self):
    #     return {'domain': {'consumable_ids': [('detailed_type', '=', 'consu')]}}

        

class newfield(models.Model):
    _name='user.resources'
    _description='resources'

    user_id= fields.Many2one('res.users', string='Resources')
    days= fields.Integer(string = 'Days')
    crm_id=fields.Many2one('crm.lead', string='crm')

# class project(models.Model):
#     _inherit='project.project'

#     custom_note= fields.Char(string = 'Notes', related='sale_order_id.custom_note')
