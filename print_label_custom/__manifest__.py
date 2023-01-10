{
  'name' : 'custom print label report',
  'version' : '1.0.0',
  'category' : 'Report',
  'sequence': -100,
  'summary' : 'custom report',
  'description' : """custom report""",
  'depends':  ['crm' , 'sale_management' , 'sale_crm' , 'project' ,'product'],
  'data':  [
     'security/ir.model.access.csv',
    'views/new_button.xml',
    'wizard/product_label_layout_views.xml',

    'report/printlabel_custom_report_template.xml',
    # 'report/report_button.xml',
    # # 'report/product_temp.xml',
   ],

  'demo':[],
  'application':  True,
  'auto_install':  False,
  'license': 'LGPL-3',
}