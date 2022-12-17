from odoo import api, fields, models
from odoo.exceptions import UserError

#  crm model 
class crm(models.Model):
    _inherit='crm.lead'

    with_whom= fields.Char(string = 'With Whom')
    how_long= fields.Char(string = 'How Long')
    alone_or_two= fields.Char(string = 'Alone Or With 2')
    contact_person= fields.Char(string = 'Contact Person')
    todos= fields.Html(string = 'Todos')
    location_material= fields.Text(string = 'Location And Material')
    extra_information= fields.Html(string = 'Extra Information')
    material_and_tools_ids= fields.Many2many('product.product', string='Material and Tools')
    consumable_ids = fields.Many2many('product.product', 'product_product_costum')
    resource_ids=fields.One2many('user.resources','crm_id',string='Resource Id')
    date_ids=fields.One2many('user.resources','crm_id',string='Date')
        

class newfield(models.Model):
    _name='user.resources'
    _description='resources'

    user_id= fields.Many2one('res.users', string='Resources')
    days= fields.Integer(string = 'Days')
    crm_id=fields.Many2one('crm.lead', string='crm')
    date= fields.Date(string = 'Customer Availability Date')
    from_time=fields.Float(string='From')
    to_time=fields.Float(string='To')

# crm model ends here!

# sale model
class sale(models.Model):
    _inherit='sale.order' 
   
    sale_with_whom= fields.Char(string = 'With Whom' , related='opportunity_id.with_whom')
    sale_how_long= fields.Char(string = 'How Long' , related='opportunity_id.how_long')
    sale_alone_or_two= fields.Char(string = 'Alone Or With 2' , related='opportunity_id.alone_or_two')
    sale_contact_person= fields.Char(string = 'Contact Person', related='opportunity_id.contact_person') 
    sale_todos= fields.Html(string = 'Todos', related='opportunity_id.todos')
    sale_location_material= fields.Text(string = 'Location And Material', related='opportunity_id.location_material')
    sale_extra_information= fields.Html(string = 'Extra Information', related='opportunity_id.extra_information')
    sale_material_and_tools_ids= fields.Many2many('product.product', string='Material and Tools' , related='opportunity_id.material_and_tools_ids')
    # consumable_ids= fields.Many2many('product.product', string='Consumable')
    sale_consumable_ids = fields.Many2many('product.product', 'product_product_custom' , string='Consumable' , related='opportunity_id.consumable_ids')  
    
    sale_resource_ids=fields.One2many('user.resources',string='Resource Id',related='opportunity_id.resource_ids')
    sale_date_ids=fields.One2many('user.resources',string='Date' ,related='opportunity_id.date_ids' )            


# project model
class project(models.Model):
    _inherit='project.project' 

    project_with_whom= fields.Char(string = 'With Whom' , related='sale_order_id.sale_with_whom')
    project_how_long= fields.Char(string = 'How Long' , related='sale_order_id.sale_how_long')
    project_alone_or_two= fields.Char(string = 'Alone Or With 2' , related='sale_order_id.sale_alone_or_two')
    project_contact_person= fields.Char(string = 'Contact Person' , related='sale_order_id.sale_contact_person')
    project_todos= fields.Html(string = 'Todos' , related='sale_order_id.sale_todos')
    project_location_material= fields.Text(string = 'Location And Material' , related='sale_order_id.sale_location_material')
    project_extra_information= fields.Html(string = 'Extra Information' , related='sale_order_id.sale_extra_information')
    project_material_and_tools_ids= fields.Many2many('product.product', string='Material and Tools' , related='sale_order_id.sale_material_and_tools_ids')
    # consumable_ids= fields.Many2many('product.product', string='Consumable')
    project_consumable_ids = fields.Many2many('product.product', 'product_product_costom' , string='Consumable' , related='sale_order_id.sale_consumable_ids')  

    project_resource_ids=fields.One2many('user.resources',string='Resource Id',related='sale_order_id.sale_resource_ids')
    project_date_ids=fields.One2many('user.resources',string='Date',related='sale_order_id.sale_date_ids')