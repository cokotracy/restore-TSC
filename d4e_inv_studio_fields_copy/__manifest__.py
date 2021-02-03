# -*- coding: utf-8 -*-
{
    'name': "Invoice Studio Fields Copy",


    'description': """
        Invoice Studio Fields Copy
    """,

    'author': "D4E",
    'website': "https://www.d4e.cool",
    'category': 'Tools',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

}
