# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    is_package = fields.Boolean('Package')

