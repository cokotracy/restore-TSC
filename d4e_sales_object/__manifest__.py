# -*- coding: utf-8 -*-
{
    'name': "Sales Object",

    'description': """
        Sales Object
    """,

    'author': "D4E",
    'category': 'Tools',
    'website': 'https://www.d4e.cool',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],

}
