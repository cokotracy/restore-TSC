from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    situation_account = fields.Many2one('account.account', default_model='account.move.line',
                                        string='Situation Account')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            situation_account=int(
                self.env['ir.config_parameter'].sudo().get_param('d4e_invoice_situation.situation_account')),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        field1 = self.situation_account and self.situation_account.id or False
        param.set_param('d4e_invoice_situation.situation_account', field1)
