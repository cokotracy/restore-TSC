from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_number = fields.Char('Customer Number')

    @api.model
    def create(self, vals):
        if not vals.get('parent_id'):
            sequence =  self.env['ir.sequence'].next_by_code(
                'res.partner', sequence_date=None)
            vals['customer_number'] = sequence
        return super(ResPartner, self.with_context({'create': True})).create(vals)

    def write(self, vals):
        ctx = self.env.context.copy()
        for rec in self:
            if not rec.customer_number and not vals.get('parent_id') and 'create' not in ctx:
                sequence =  self.env['ir.sequence'].next_by_code(
                    'res.partner', sequence_date=None)
                vals['customer_number'] = sequence
        return super(ResPartner, self).write(vals)