# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    contract_end_date = fields.Date('Contrat end date')


    #using cron send mail to user for quotation expiration details#
    def _action_cron(self):
        employees = self.search([('contract_end_date','!=',False)])
        param = self.env['ir.config_parameter'].sudo()
        remind_before = int(param.get_param('d4e_contract_end.remind_before'))
        send_to = param.get_param('d4e_contract_end.send_to')
        print(remind_before)
        print(send_to)

        template_id = self.env.ref('d4e_contract_end.contract_expiration_mail_inherit')
        today = datetime.now().date()
        frequency = str(remind_before) + " Week(s)"
        for employee in employees:
            if send_to == 'employee':
                partner = employee.user_partner_id
            elif send_to == 'other':
                p = int(param.get_param('d4e_contract_end.partner_id'))
                partner = self.env['res.partner'].search([('id','=',p)])

            email_list = []
            expiry_date = employee.contract_end_date
            reminder_date = (datetime.strptime(str(expiry_date),"%Y-%m-%d") - relativedelta(weeks=remind_before)).date()
            if today == reminder_date:
                if template_id:
                   template_id.with_context({'frequency':frequency,'email_to': partner.email}).send_mail(partner.id ,force_send=True)


