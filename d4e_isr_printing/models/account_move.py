# -*- coding: utf-8 -*-

from odoo import api, fields, models, http
from odoo.tools import pdf

import base64

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _pdf_invoices_with_isr(self, invoice_ids):
        pdf_docs = []
        actions = [
            http.request.env.ref('account.account_invoices'),
            http.request.env.ref('l10n_ch.l10n_ch_isr_report'),
        ]

        for invoice_id in invoice_ids:
            pdf_data = actions[0].render_qweb_pdf(invoice_id)[0]
            pdf_docs.append(pdf_data)

            active_invoice = http.request.env['account.move'].browse(invoice_id)

            if active_invoice and active_invoice.l10n_ch_isr_valid:
                active_invoice.l10n_ch_isr_sent = True
                isr_data = actions[1].render_qweb_pdf(invoice_id)[0]
                pdf_docs.append(isr_data)

        pdf_merge = pdf.merge_pdf(pdf_docs)
        return pdf_merge


class AccountMoveController(http.Controller):

    @http.route('/report/isr/<active_ids>', auth='user')
    def report_isr(self, active_ids):
        invoice_ids = []

        for active_id in active_ids.split(','):
            invoice_ids.append(int(active_id))

        pdf_merge = http.request.env['account.move']._pdf_invoices_with_isr(invoice_ids)
        pdf_http_headers = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf_merge))]
        return http.request.make_response(pdf_merge, headers=pdf_http_headers)
