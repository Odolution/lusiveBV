{
  'name' : 'custom field for crm',
  'version' : '1.0.0',
  'category' : 'CRM',
  'sequence': -100,
  'summary' : 'custom field for crm',
  'description' : """custom field for crm""",
  'depends':  ['crm' , 'sale_management' , 'sale_crm' , 'project' ,'sale_project'],
  'data':  [
     'security/ir.model.access.csv',
     'views/distributor_view.xml',  
   ],

  'demo':[],
  'application':  True,
  'auto_install':  False,
  'license': 'LGPL-3',
}