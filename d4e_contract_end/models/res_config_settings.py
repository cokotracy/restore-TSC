from odoo import models, fields, api, _

class ResConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    remind_before = fields.Integer('Remind Before', default=2)

    send_to = fields.Selection([('employee','Employee'),('other','Other')],
                               default='employee', string="Send To")

    partner_id = fields.Many2one('res.partner','person')

    @api.model
    def get_values(self):
        res = super(ResConfiguration, self).get_values()
        param = self.env['ir.config_parameter'].sudo()
        res.update(
            remind_before = int(param.get_param('d4e_contract_end.remind_before')),
            send_to = param.get_param('d4e_contract_end.send_to'),
            partner_id = int(param.get_param('d4e_contract_end.partner_id')),
        )
        return res


    def set_values(self):
        super(ResConfiguration, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        field1 = self.remind_before
        field2 = self.send_to
        field3 = self.partner_id and self.partner_id.id or False

        param.set_param('d4e_contract_end.remind_before', field1)
        param.set_param('d4e_contract_end.send_to', field2)
        param.set_param('d4e_contract_end.partner_id', field3)


