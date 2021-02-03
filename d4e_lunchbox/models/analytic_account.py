from odoo import models, fields, api
from datetime import datetime
from dateutil import parser
from pandas import pandas as pd

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    lunchbox = fields.Boolean('Lunchbox', compute='_compute_lunchbox',store=True)

    @api.depends('employee_id', 'unit_amount','date')
    def _compute_lunchbox(self):
        all_employees = self.mapped('employee_id')
        for rec in self:
            if rec.unit_amount > 5:
                rec.lunchbox = True
            else:
                rec.lunchbox = False

            for employee in all_employees:
                groupby_date = rec.read_group(
                    domain=[('employee_id', '=', employee.id),],
                    fields=['date', 'unit_amount'],
                    groupby=['date:day'])
                for group in groupby_date:
                    if group['date_count'] > 1 and group['unit_amount'] > 5:
                        date = None
                        month = group['date:day'].split()[1]
                        day = group['date:day'].split()[0]
                        year = group['date:day'].split()[2]
                        if self.env.lang and self.env.lang == 'fr_CH':
                            frenc_to_num = {u'janv.': u'1', u'févr.': u'2',u'mars': u'3',u'avr.': u'4',
                                            u'mai': u'5', u'juin': u'6',u'juil.': u'7', u'août': u'8',
                                            u'sept.': u'9', u'oct.': u'10', u'nov.': u'11', u'déc.': u'12'}
                            m = frenc_to_num[month]
                            date = pd.to_datetime(year + '-' + m + '-' + day,format='%Y-%m-%d', errors='ignore').date()
                        elif self.env.lang and self.env.lang == 'en_US':
                            eng_to_num = {u'Jan': u'1', u'Feb': u'2', u'Mar': u'3', u'Apr': u'4',
                                            u'May': u'5', u'Jun': u'6', u'Jul': u'7', u'Aug': u'8',
                                            u'Sep': u'9', u'Oct': u'10', u'Nov': u'11', u'Dec': u'12'}
                            m = eng_to_num[month]
                            date = pd.to_datetime(year + '-' + m + '-' + day,format='%Y-%m-%d', errors='ignore').date()
                        res = self.search([('employee_id', '=', employee.id),
                                          ('date', '=', date)])
                        if len(res) > 0 and not any(r.lunchbox == True for r in res):
                            res[0].lunchbox = True

    custom_amounts_list = fields.Many2one('custom.amount', 'Amounts List')
    custom_amount = fields.Float('Amount')
    real_amount = fields.Float('Lunchbox Amount', compute='compute_real_amount', store=True)

    @api.depends('custom_amounts_list','custom_amount')
    def compute_real_amount(self):
        for rec in self:
            if rec.custom_amounts_list:
                rec.real_amount = rec.custom_amounts_list.value
            elif rec.custom_amount != 0:
                rec.real_amount = rec.custom_amount
            else:
                rec.real_amount = 0

    def copy(self,default=None):
        default = dict(default or {})
        default['date'] = self.date
        default['weeknumber'] = self.weeknumber
        default['employee_id'] = self.employee_id.id
        default['name'] = self.name
        default['project_id'] = self.project_id.id
        default['task_id'] = self.task_id.id
        default['unit_amount'] = self.unit_amount
        default['lunchbox'] = self.lunchbox
        default['custom_amounts_list'] = self.custom_amounts_list.id
        default['custom_amount'] = self.custom_amount
        default['real_amount'] = self.real_amount
        return super(AccountAnalyticLine, self).copy(default)

    def _timesheet_postprocess_values(self, values):
        # res = super(AccountAnalyticLine,self)._timesheet_postprocess_values(values)
        result = {id_: {} for id_ in self.ids}
        sudo_self = self.sudo()  # this creates only one env for all operation that required sudo()
        # (re)compute the amount (depending on unit_amount, employee_id for the cost, and account_id for currency)
        if any([field_name in values for field_name in ['unit_amount', 'employee_id', 'account_id']]):
            for timesheet in sudo_self:
                cost = (timesheet.employee_id.timesheet_cost) or 0.0
                print('timesheet.real_amount: ',timesheet.real_amount)
                amount = (-timesheet.unit_amount * cost) - timesheet.real_amount
                print('amount: ',amount)
                amount_converted = timesheet.employee_id.currency_id._convert(
                    amount, timesheet.account_id.currency_id, self.env.company, timesheet.date)

                print('amount_converted: ',amount_converted)

                result[timesheet.id].update({
                    'amount': amount_converted,
                })
        return result

class CustomAmount(models.Model):
    _name = 'custom.amount'

    name = fields.Char('Name', compute='compute_name', store=True)
    value = fields.Float('Amount Value')

    @api.depends('value')
    def compute_name(self):
        for rec in self:
            rec.name = str(rec.value)
