# -*- coding: utf-8 -*-
{
    'name': "Custom Reports",

    'description': """
        Custom Reports
    """,

    'author': "D4E",
    'website': "https://www.d4e.cool",
    'category': 'Tools',
    'version': '1.0',

    'depends': ['base','account','sale','web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/invoice_report.xml',
        'views/saleorder_report.xml',
    ],

}
