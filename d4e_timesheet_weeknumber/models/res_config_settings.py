
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    def recompute_weeknumber_values(self):
        model = self.env['account.analytic.line']
        lines = model.search([])
        for line in lines:
            line._compute_week_number()