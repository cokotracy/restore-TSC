# -*- coding: utf-8 -*-
{
    'name': "Employee Lunchbox",

    'description': """
        Employee Lunchbox
    """,

    'author': "D4E",
    'website': "http://www.d4e.cool",
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_timesheet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
