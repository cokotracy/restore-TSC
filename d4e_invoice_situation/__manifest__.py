# -*- coding: utf-8 -*-
{
    'name': "Invoice Situation",

    'description': """
        Invoice Situation
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
        'views/invoice_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/sale_make_inv_advance.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
