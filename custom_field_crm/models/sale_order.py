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
    # consumable_ids= fields.Many2many('product.product', string='Consumable')
    consumable_ids = fields.Many2many('product.product', 'product_product_costum')

    resource_ids=fields.One2many('user.resources','crm_id',string='Resource Id')
    date_ids=fields.One2many('user.resources','crm_id',string='Date')
    
    
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
    
    # sale_resource_ids=fields.One2many('sale.resources','sale_id',string='Resource Id')
    sale_resource_ids=fields.One2many('user.resources',string='Resource Id',related='opportunity_id.resource_ids')
    sale_date_ids=fields.One2many('user.resources',string='Date' ,related='opportunity_id.date_ids' )

    # @api.onchange('opportunity_id')
    # def opportunity_ids_onchange(self):
    #     for rec in self:
    #                 rec["sale_with_whom"]=self.opportunity_id.with_whom
    #                 rec["sale_how_long"]=self.opportunity_id.how_long
    #                 rec["sale_alone_or_two"]=self.opportunity_id.alone_or_two
    #                 rec["sale_contact_person"]=self.opportunity_id.contact_person
    #                 rec["sale_todos"]=self.opportunity_id.todos
    #                 rec["sale_location_material"]=self.opportunity_id.location_material
    #                 rec["sale_extra_information"]=self.opportunity_id.extra_information
    #                 rec["sale_material_and_tools_ids"]=self.opportunity_id.material_and_tools_ids
    #                 rec["sale_consumable_ids"]=self.opportunity_id.consumable_ids

            

class sale_newfield(models.Model):
    _name='sale.resources'
    _description=' Sale resources'
    
    

    # sale_user_id= fields.Many2one('res.users', string='Resources')
    # sale_days= fields.Integer(string = 'Days')
    # sale_id=fields.Many2one('sale.order', string='sale')
    # sale_date= fields.Date(string = 'Customer Availability Date')
    # sale_from_time=fields.Float(string='From')
    # sale_to_time=fields.Float(string='To')

    # sale_user_id= fields.Many2one('res.users', string='Resources' , related='opportunity_id.user_id')
    # sale_days= fields.Integer(string = 'Days' , related='opportunity_id.days')
    # sale_id=fields.Many2one('sale.order', string='sale' , related='opportunity_id.crm_id')
    # sale_date= fields.Date(string = 'Customer Availability Date' , related='opportunity_id.date')
    # sale_from_time=fields.Float(string='From' , related='opportunity_id.from_time')
    # sale_to_time=fields.Float(string='To' , related='opportunity_id.to_time')


    # @api.onchange('opportunity_id')
    # def item_delivered_ids_onchange(self):
    #     for rec in self:
    #                 rec["sale_user_id"]=self.opportunity_id.user_id
    #                 rec["sale_days"]=self.opportunity_id.days
    #                 rec["sale_date"]=self.opportunity_id.date
    #                 rec["sale_from_time"]=self.opportunity_id.from_time
    #                 rec["sale_to_time"]=self.opportunity_id.to_time
                    
# sale model ends here


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

    project_resource_ids=fields.One2many('project.resources','project_id',string='Resource Id')
    project_date_ids=fields.One2many('project.resources','project_id',string='Date')


    # @api.onchange('sale_order_id' ,'sale_line_id')
    # def opportunity_ids_onchange(self):
    #     # UserError['in method']
    #     for rec in self:
    #                 rec["project_with_whom"]=rec.sale_order_id.sale_with_whom
    #                 rec["project_how_long"]=rec.sale_order_id.sale_how_long
    #                 rec["project_alone_or_two"]=rec.sale_order_id.sale_alone_or_two
    #                 rec["project_contact_person"]=rec.sale_order_id.sale_contact_person
    #                 rec["project_todos"]=rec.sale_order_id.sale_todos
    #                 rec["project_location_material"]=rec.sale_order_id.sale_location_material
    #                 rec["project_extra_information"]=rec.sale_order_id.sale_extra_information
    #                 rec["project_material_and_tools_ids"]=rec.sale_order_id.sale_material_and_tools_ids
    #                 rec["project_consumable_ids"]=rec.sale_order_id.sale_consumable_ids

class project_newfield(models.Model):
    _name='project.resources'
    _description=' project resources'
   
    
    project_user_id= fields.Many2one('res.users', string='Resources')
    project_days= fields.Integer(string = 'Days')
    project_id=fields.Many2one('project.project', string='Project')
    project_date= fields.Date(string = 'Customer Availability Date')
    project_from_time=fields.Float(string='From')
    project_to_time=fields.Float(string='To')

    # project_user_id= fields.Many2one('res.users', string='Resources' , related='sale_order_id.sale_user_id')
    # project_days= fields.Integer(string = 'Days' , related='sale_order_id.sale_days')
    # project_id=fields.Many2one('project.project', string='Project' , related='sale_order_id.sale_id')
    # project_date= fields.Date(string = 'Customer Availability Date' , related='sale_order_id.sale_date')
    # project_from_time=fields.Float(string='From' , related='sale_order_id.sale_from_time')
    # project_to_time=fields.Float(string='To' , related='sale_order_id.sale_to_time')
# project model ends here!




# class project(models.Model):
#     _inherit='project.project'

#     custom_note= fields.Char(string = 'Notes', related='sale_order_id.custom_note')

