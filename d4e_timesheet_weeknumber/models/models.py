# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    weeknumber = fields.Char('Week Number', compute='_compute_week_number',store=True)

    @api.depends('date')
    def _compute_week_number(self):
        for line in self:
            date = line.date
            line.weeknumber = date.strftime('%V - %Y')
