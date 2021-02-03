from odoo import models, fields


class SaleSplitAmount(models.Model):
    _name = 'sale.split.amount'
    _description = '''Sale Split Amount'''

    order_id = fields.Many2one('sale.order', 'Sale Order')
    amount = fields.Float('Amount')
    expected_date = fields.Date('Expected Date')
