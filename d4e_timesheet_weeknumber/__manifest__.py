# -*- coding: utf-8 -*-
{
    'name': "Timesheet Week Number",

    'description': """
        Timesheet Week Number
    """,

    'author': "D4E",
    'website': "http://www.d4e.cool",
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_timesheet'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/res_config_settings.xml',
    ],

}
