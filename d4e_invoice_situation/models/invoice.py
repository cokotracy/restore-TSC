# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = 'account.move'

    is_situation = fields.Boolean('Situation')


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    is_situation = fields.Boolean(related='move_id.is_situation',string='Situation')

#     def _get_situation_account_id(self):
#         return self.env['ir.config_parameter'].sudo().get_param('d4e_invoice_situation.situation_account') or False
#
#     @api.model
#     def create(self, values):
#         order = self.env['account.move'].search([('id','=',values['move_id'])])
#         if order.is_situation:
#             values.update({'account_id': self._get_situation_account_id()})
#         return super(InvoiceLine, self).create(values)
#
