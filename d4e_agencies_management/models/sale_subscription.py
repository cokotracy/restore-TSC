import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, _


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    agency_id = fields.Many2one('agency.agency', 'Agency')
    date_stop = fields.Date('Date Stop')

    def generate_sales(self):

        months = self.diff_month(self.date_stop, self.date_start)
        orders = []
        for month in range(months):
            for subscription in self:
                order_lines = []
                fpos_id = self.env['account.fiscal.position'].get_fiscal_position(subscription.partner_id.id)
                for line in subscription.recurring_invoice_line_ids:
                    order_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.product_id.product_tmpl_id.name,
                        'subscription_id': subscription.id,
                        'product_uom': line.uom_id.id,
                        'product_uom_qty': line.quantity,
                        'price_unit': line.price_unit,
                        'discount': line.discount,
                    }))
                addr = subscription.partner_id.address_get(['delivery', 'invoice'])
                sale_order = self.env['sale.order'].search([
                    ('order_line.subscription_id', 'in', self.ids)
                ], order="id desc", limit=1)
                vals = {
                    'pricelist_id': subscription.pricelist_id.id,
                    'partner_id': subscription.partner_id.id,
                    'partner_invoice_id': addr['invoice'],
                    'partner_shipping_id': addr['delivery'],
                    'currency_id': subscription.pricelist_id.currency_id.id,
                    'order_line': order_lines,
                    'analytic_account_id': subscription.analytic_account_id.id,
                    'subscription_management': 'renew',
                    'origin': subscription.code,
                    'note': subscription.description,
                    'fiscal_position_id': fpos_id,
                    'user_id': subscription.user_id.id,
                    'payment_term_id': sale_order.payment_term_id.id if sale_order else subscription.partner_id.property_payment_term_id.id,
                    'company_id': subscription.company_id.id,
                    'agency_id': subscription.agency_id.id
                }
                order = self.env['sale.order'].create(vals)
                order.write({
                    'date_order': self.date_start + relativedelta(months=month),
                })
                order.action_confirm()
                orders.append(order.id)

        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Orders'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', orders)],
        }

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month + 1
