# -*- coding: utf-8 -*-
{
    'name': "Sales Package",

    'description': """
        Sales Package
    """,

    'author': "D4E",
    'category': 'Tools',
    'website': 'https://www.d4e.cool',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/invoice_views.xml',
        'views/sale_order_views.xml',
        'views/invoice_report.xml',
        'views/sale_order_report.xml',

    ],

}
