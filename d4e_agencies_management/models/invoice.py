from odoo import models, fields, api,_
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    agency_id = fields.Many2one('agency.agency', 'Agency')
    project_id = fields.Many2one('project.project', 'Projet')
    note = fields.Text('Note')

    @api.onchange('project_id')
    def partner_project_change(self):
        if self.type == 'out_invoice':
            if self.project_id:
                self.partner_id = self.project_id.partner_id.id
                self.agency_id = self.project_id.agency_id.id
            if self.invoice_line_ids:
                for line in self.invoice_line_ids:
                    line.analytic_account_id = self.project_id.analytic_account_id


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'product_uom_id' in vals and vals['product_uom_id'] != False :
                move = self.env['account.move'].browse(vals['move_id'])
                vals['analytic_account_id'] = move.project_id.analytic_account_id.id
        lines = super(AccountMoveLine, self).create(vals_list)
        moves = lines.mapped('move_id')
        if self._context.get('check_move_validity', True):
            moves._check_balanced()
        print(self._context.get('check_move_validity'))
        moves._check_fiscalyear_lock_date()
        lines._check_tax_lock_date()
        # moves._recompute_dynamic_lines(recompute_all_taxes=True, recompute_tax_base_amount=True)
        return lines
