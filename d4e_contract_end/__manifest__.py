# -*- coding: utf-8 -*-
{
    'name': "Contract End Track",

    'description': """
        Contract End Track
    """,

    'author': "D4E",
    'website': "https://www.d4e.cool",
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/contract_expiration_cron.xml',
        'data/expiration_mail_template_data.xml',
        'views/res_config_settings_view.xml',
        'views/employee_views.xml',
    ],

}
