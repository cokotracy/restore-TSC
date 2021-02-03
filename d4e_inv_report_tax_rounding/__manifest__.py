# -*- coding: utf-8 -*-
{
    'name': "Invoice Report Tax & Cash Rounding",

    'description': """
        Invoice Report Tax & Cash Rounding
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
        'views/invoice_report_template.xml',
    ],

}
