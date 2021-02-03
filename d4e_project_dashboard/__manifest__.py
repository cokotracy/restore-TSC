# -*- coding: utf-8 -*-
{
    'name': "Project Dashboard",
    'summary': """ Project Dashboard """,
    'description': """
        Project Dashboard
    """,
    'author': "D4E",
    'website': "http://www.d4e.cool",
    'category': 'Project',
    'version': '13.0',

    'depends': ['project',
                'account',
                'sale',
                'hr_timesheet',
                'sale_timesheet',
                'd4e_agencies_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/project_dashboard_views.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],

    'installable': True,
    'application': True,
}