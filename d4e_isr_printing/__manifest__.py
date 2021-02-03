# -*- coding: utf-8 -*-
{
    'name': "d4e_isr_printing",

    'summary': """
        Digital4Efficiency - ISR Mass Printing
    """,

    'description': """
        Mass print ISRs with invoices.
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    'version': '0.0.1',

    'depends': [
        'account_accountant',
        'l10n_generic_coa',
        'l10n_ch',
        'web'
    ],

    'data': [
        'data/server_actions.xml',
        'report/isr_report.xml',
    ],
}
