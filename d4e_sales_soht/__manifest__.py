# -*- coding: utf-8 -*-
{
    'name': "Sales HT",

    'description': """
        Sales HT
    """,

    'author': "D4E",
    'category': 'Tools',
    'website': 'https://www.d4e.cool',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/saleorder_report.xml',
        'views/invoice_report.xml',
    ],

    'installable': True,
    'application': False,
}
