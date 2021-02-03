from datetime import date, datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTM


class ProjectProject(models.Model):
    _inherit = 'project.project'

    agency_id = fields.Many2one(
        'agency.agency',
        string='Agency',
    )

    sale_order_ids = fields.One2many(
        'sale.order',
        'project_id',
        string='Quotations / Sales Orders'
    )
    description = fields.Text('Description')

    invoice_ids = fields.One2many('account.move','project_id','Invoices')


    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.analytic_account_id.write({'name': self.name})


class ProjectTask(models.Model):
    _inherit = 'project.task'

    agency_id = fields.Many2one(
        'agency.agency',
        string='Agency',
        related='project_id.agency_id',
        store=True
    )
