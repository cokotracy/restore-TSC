from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agency_id = fields.Many2one('agency.agency', 'Agency')
    split_amount_ids = fields.One2many(
        'sale.split.amount',
        'order_id',
        string='Split Amount'
    )
    total_split = fields.Float(compute='compute_total_split', store=True)
    project_id = fields.Many2one(
        'project.project', 'Project',
        readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help='Select a non billable project on which tasks can be created.')

    custom_note = fields.Text('Note', translate=True)
    customer_ref = fields.Char('Customer Reference')

    @api.depends('split_amount_ids.amount')
    def compute_total_split(self):
        self.total_split = sum([p.amount for p in self.split_amount_ids])

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        to_update = {
            'state': 'sale',
        }
        if not self.split_amount_ids:
            vals = {
                'amount': self.amount_untaxed,
                'expected_date': self.date_order
            }
            to_update['split_amount_ids'] = [(0, 0, vals)]
        self.write(to_update)
        self._action_confirm()
        if self.amount_untaxed != self.total_split:
            raise UserError(_('The total amount of lines on planning tab must be equal to the total amount.'))
        if not self.customer_ref:
            raise UserError(_('You must enter a customer ref to confirm quotation !'))
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True

    # @api.constrains('amount_total', 'total_split', 'state')
    # def _check_amount(self):
    #     for s in self:
    #         if s.total_split != s.amount_untaxed and s.state not in ['draft', 'sent', 'cancel']:
    #             raise ValidationError(_('The total amount of lines on planning tab must be equal to the total amount.'))

    @api.model
    def create(self, vals):
        old_so = self.search_count([])
        sequence = 'DEV{}'.format(
            str(old_so + 1).zfill(6)
        )
        vals['name'] = sequence
        print(sequence)
        return super(SaleOrder, self).create(vals)

    @api.onchange('project_id')
    def partner_project_change(self):
        if self.project_id:
            self.partner_id = self.project_id.partner_id.id
            self.agency_id = self.project_id.agency_id.id

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            value = {'domain': {'project_id': [('partner_id', '=', self.partner_id.id)]}}
            return value

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({
            'project_id': self.project_id.id,
            'ref': self.customer_ref,
            'agency_id': self.agency_id.id,
        })
        return res

    def _create_invoices(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        # 1) Create invoices.
        invoice_vals_list = []
        for order in self:
            pending_section = None
            if order.custom_note:
                note = order.custom_note + _("\nRealized during the week")
            else:
                note = ""
            note_line = (0, 0, {
                'display_type': 'line_note',
                'name': note,
                'sequence': 11,
                'account_id': False,

            })
            # Invoice values.
            invoice_vals = order._prepare_invoice()

            # Invoice line values (keep only necessary sections).
            for line in order.order_line:
                if line.display_type == 'line_section':
                    pending_section = line
                    continue
                if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                    continue
                if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final):
                    if pending_section:
                        invoice_vals['invoice_line_ids'].append((0, 0, pending_section._prepare_invoice_line()))
                        pending_section = None
                    invoice_vals['invoice_line_ids'].append((0, 0, line._prepare_invoice_line()))

            if not invoice_vals['invoice_line_ids']:
                raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise UserError(_(
                'There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

        # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
        if not grouped:
            new_invoice_vals_list = []
            for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: (x.get('partner_id'), x.get('currency_id'))):
                origins = set()
                payment_refs = set()
                refs = set()
                ref_invoice_vals = None
                for invoice_vals in invoices:
                    if not ref_invoice_vals:
                        ref_invoice_vals = invoice_vals
                    else:
                        ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                    origins.add(invoice_vals['invoice_origin'])
                    payment_refs.add(invoice_vals['invoice_payment_ref'])
                    refs.add(invoice_vals['ref'])
                ref_invoice_vals.update({
                    'ref': ', '.join(refs),
                    'invoice_origin': ', '.join(origins),
                    'invoice_payment_ref': len(payment_refs) == 1 and payment_refs.pop() or False,
                })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

        # 3) Manage 'final' parameter: transform out_invoice to out_refund if negative.
        out_invoice_vals_list = []
        refund_invoice_vals_list = []
        if final:
            for invoice_vals in invoice_vals_list:
                if sum(l[2]['quantity'] * l[2]['price_unit'] for l in invoice_vals['invoice_line_ids']) < 0:
                    for l in invoice_vals['invoice_line_ids']:
                        l[2]['quantity'] = -l[2]['quantity']
                    invoice_vals['type'] = 'out_refund'
                    invoice_vals['invoice_line_ids'].append(note_line)
                    refund_invoice_vals_list.append(invoice_vals)
                else:
                    invoice_vals['invoice_line_ids'].append(note_line)
                    out_invoice_vals_list.append(invoice_vals)
        else:
            invoice_vals['invoice_line_ids'].append(note_line)
            out_invoice_vals_list = invoice_vals_list

        if invoice_vals['type'] in self.env['account.move'].get_outbound_types():
            invoice_bank_id = self.partner_id.bank_ids[:1]
        else:
            invoice_bank_id = self.company_id.partner_id.bank_ids[:1]

        invoice_vals['invoice_partner_bank_id'] = invoice_bank_id

        # Create invoices.
        moves = self.env['account.move'].with_context(default_type='out_invoice').create(out_invoice_vals_list)
        moves += self.env['account.move'].with_context(default_type='out_refund').create(refund_invoice_vals_list)
        for move in moves:
            move.message_post_with_view('mail.message_origin_link',
                values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                subtype_id=self.env.ref('mail.mt_note').id
            )
        return moves

