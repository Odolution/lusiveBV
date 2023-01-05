# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Custom Calender View",

    "author": "Odolution",
    "category": "sale",

    "license": "OPL-1",

    "version": "15.0.1",

    "depends": ['calendar'],
    # 'qweb': ['custom_calendar/static/src/xml/calendar_service.xml'],

    "assets"               :  {
                             
                              
                              'web.assets_qweb': [
                                'custom_calendar/static/src/xml/calendar_service.xml',
                              ],
                            },
    "data": [
        'views/main_view.xml',
        ],
    
    "images": [ ],
    "auto_install": False,
    "application": True,
    "installable": True,
}
