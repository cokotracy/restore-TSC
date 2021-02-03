# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Agencies Management',
    'version': '1.0',
    'description': """
    Agencies Management
""",
    'Author': 'D4E',
    'category': 'Tools',
    'website': 'https://www.d4e.cool',
    'depends': [
        'sale',
        'project',
        'sale_timesheet',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/sale_views.xml',
        'views/project_views.xml',
        'views/agency_views.xml',
        'views/invoice_views.xml',
        'views/partner_view.xml',
        # Reports
        'report/agencies_report.xml',
        # Data
        'data/sequences.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
