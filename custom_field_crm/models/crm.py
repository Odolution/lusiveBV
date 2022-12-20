from odoo import api, fields, models
from odoo.exceptions import UserError

#  crm model 
class crm(models.Model):
    _inherit='crm.lead'


    invoice=fields.Many2one('res.partner', string='Invoice')
    delivery=fields.Many2one('res.partner', string='Delivery')
    contact_person= fields.Text(string = 'Contact Person')
    todos= fields.Html(string = 'Todos')
    
    sale_location_material= fields.Text(string = 'Location And Material')
    consumable_ids = fields.Many2many('product.product', 'product_product_costum')
    resource_ids=fields.One2many('user.resources','crm_id',string='Resource Id')
    date_ids=fields.One2many('user.resources','crm_id',string='Date')
    material_ids=fields.Many2many('material.tools',string='Material')
        

class newfield(models.Model):
    _name='user.resources'
    _description='resources'

    user_id= fields.Many2one('res.users', string='Resources')
    hours= fields.Float(string='Hours')
    information= fields.Text(string='Information')
    crm_id=fields.Many2one('crm.lead', string='crm')
    date= fields.Date(string = 'Customer Availability Date')
    from_time=fields.Float(string='From')
    to_time=fields.Float(string='To')

class new_material(models.Model):
    _name='material.tools'
    _description='material and tools'
    name=fields.Char(string="name")
    # material_and_tools_ids= fields.Char(string='Material and Tools')
    # crm_ids=fields.Many2one('crm.lead', string='crm')

    

# crm model ends here!

# sale model
class sale(models.Model):
    _inherit='sale.order' 
   
    sale_contact_person= fields.Text(string = 'Contact Person', related='opportunity_id.contact_person') 
    sale_todos= fields.Html(string = 'Todos', related='opportunity_id.todos')
    # sale_location_material= fields.Text(string = 'Location And Material', related='opportunity_id.location_material')
    # consumable_ids= fields.Many2many('product.product', string='Consumable')
    # sale_material_and_tools_ids= fields.Many2many('material.tools', string='Material and Tools' , related='opportunity_id.material_and_tools_ids')
    sale_consumable_ids = fields.Many2many('product.product', 'product_product_custom' , string='Consumable' , related='opportunity_id.consumable_ids')  
    sale_material_ids=fields.Many2many('material.tools',string='Material' , related='opportunity_id.material_ids')
    sale_resource_ids=fields.One2many('user.resources',string='Resource Id',related='opportunity_id.resource_ids')
    sale_date_ids=fields.One2many('user.resources',string='Date' ,related='opportunity_id.date_ids' )   

    @api.onchange('opportunity_id')
    def opportunity_ids_onchange(self):
        for rec in self:
                    rec["partner_invoice_id"]=self.opportunity_id.invoice
                    rec["partner_shipping_id"]=self.opportunity_id.delivery         


# project model
class project(models.Model):
    _inherit='project.project' 

    project_contact_person= fields.Text(string = 'Contact Person' , related='sale_order_id.sale_contact_person')
    project_todos= fields.Html(string = 'Todos' , related='sale_order_id.sale_todos')
    # project_material_and_tools_ids= fields.Many2many('material.tools', string='Material and Tools' , related='sale_order_id.sale_material_and_tools_ids')
    # consumable_ids= fields.Many2many('product.product', string='Consumable')
    project_consumable_ids = fields.Many2many('product.product', 'product_product_costom' , string='Consumable' , related='sale_order_id.sale_consumable_ids')  
    project_material_ids=fields.Many2many('material.tools',string='Material',related='sale_order_id.sale_material_ids')
    project_resource_ids=fields.One2many('user.resources',string='Resource Id',related='sale_order_id.sale_resource_ids')
    project_date_ids=fields.One2many('user.resources',string='Date',related='sale_order_id.sale_date_ids')