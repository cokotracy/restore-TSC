from odoo import models, fields, api


class Agency(models.Model):
    _name = 'agency.agency'
    _description = '''Agency Model'''

    name = fields.Char('Name', required=True)
    sequence = fields.Char('Agency Number')

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code(
            'agency.agency', sequence_date=None)
        return super(Agency, self).create(vals)
