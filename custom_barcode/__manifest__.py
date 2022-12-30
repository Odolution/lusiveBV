{
  'name' : 'custom barcode',
  'version' : '1.0.0',
  'category' : 'Barcode',
  'sequence': -100,
  'summary' : 'custom barcod',
  'description' : """custom barcod""",
  'depends':  ['crm' , 'sale_management' , 'sale_crm' , 'project' ,'product'],
  'data':  [
    #  'security/ir.model.access.csv',
    'views/location_view.xml',
    #  'report/new_order.xml',
    #  'report/report.xml',  
     'report/product_bracode.xml',
    # 'report/product_temp.xml',
   ],

  'demo':[],
  'application':  True,
  'auto_install':  False,
  'license': 'LGPL-3',
}