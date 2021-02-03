

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_dashboard = fields.Html(string="Dashboard", compute='_compute_sale_dashboard', translate=True)

    workforce = fields.Float('Worforce',compute='_compute_dashboard_values')
    various = fields.Float('Various',compute='_compute_dashboard_values')
    direct_costs = fields.Float('Direct Costs',compute='_compute_dashboard_values')
    indirect_costs = fields.Float('Indirect Costs',compute='_compute_dashboard_values')
    cost_price = fields.Float('Cost Price',compute='_compute_dashboard_values')
    billing = fields.Float('Billing',compute='_compute_dashboard_values')
    result = fields.Float('Result',compute='_compute_dashboard_values')
    nb_hours = fields.Float('Nb of Hours',compute='_compute_dashboard_values')
    hour_price = fields.Float('Price of hour',compute='_compute_dashboard_values')


    workforce_percent = fields.Float('Worforce %',compute='_compute_dashboard_values_percent')
    various_percent = fields.Float('Various %',compute='_compute_dashboard_values_percent')
    direct_costs_percent = fields.Float('Direct Costs %',compute='_compute_dashboard_values_percent')
    indirect_costs_percent = fields.Float('Indirect Costs %',compute='_compute_dashboard_values_percent')
    cost_price_percent = fields.Float('Cost Price %',compute='_compute_dashboard_values_percent')
    billing_percent = fields.Float('Billing %',compute='_compute_dashboard_values_percent')
    result_percent = fields.Float('Result %',compute='_compute_dashboard_values_percent')


    def _compute_dashboard_values(self):
        for rec in self:
            rec.workforce = 0
            rec.various = 0
            rec.direct_costs = 0
            rec.indirect_costs = 0
            rec.cost_price = 0
            rec.billing = 0
            rec.result = 0
            rec.nb_hours = 0
            rec.hour_price = 0
            project = rec.project_id

            for line in rec.order_line:
                is_benefice = (int(line.product_id.id) == int(project._get_benef_prod_id()))
                is_mo = (int(line.product_id.categ_id.id) == int(project._get_mo_categ_id()))
                is_ind_cost = (int(line.product_id.id) == int(project._get_ind_cost_prod_id()))

                if is_mo:
                    rec.workforce += line.price_subtotal
                    rec.nb_hours += line.product_uom_qty

                elif is_ind_cost:
                    rec.indirect_costs += line.price_subtotal
                elif not is_benefice:
                    rec.various += line.price_subtotal

            rec.direct_costs = rec.workforce + rec.various
            rec.billing = rec.amount_untaxed
            rec.cost_price = rec.direct_costs + rec.indirect_costs
            rec.result = rec.billing - rec.cost_price
            if rec.nb_hours != 0:
                rec.hour_price = rec.billing / rec.nb_hours
        return True


    def _compute_dashboard_values_percent(self):
        for rec in self:
            rec.workforce_percent = 0
            rec.various_percent = 0
            rec.direct_costs_percent = 0
            rec.indirect_costs_percent = 0
            rec.cost_price_percent = 0
            rec.billing_percent = 0
            rec.result_percent = 0
            billing = rec.billing

            if billing != 0:
                rec.workforce_percent = (rec.workforce * 100) / billing
                rec.various_percent = (rec.various * 100) / billing
                rec.direct_costs_percent = (rec.direct_costs * 100) / billing
                rec.indirect_costs_percent = (rec.indirect_costs * 100) / billing
                rec.cost_price_percent = (rec.cost_price * 100) / billing
                rec.billing_percent = (rec.billing * 100) / billing
                rec.result_percent = (rec.result * 100) / billing

    def _compute_sale_dashboard(self):
        for rec in self:
            rec.sale_dashboard = """
            <table style="width: 50%;">
                 <tr>
                   <th style="width:33%"> </th>
                   <th style="width:33%">""" + _('Launch') + """</th>
                   <th style="width:33%"> % </th>
                 </tr>
                 
                 <tr style="background: #e9ecef;">
                   <td>""" + _('Workforce') + """</td>
                   <td>""" + str(round(rec.workforce)) + """</td>
                   <td>""" + str(round(rec.workforce_percent, 2)) + """</td>
                 </tr>
                <tr>
                   <td>""" + _('Various') + """</td>
                   <td>""" + str(round(rec.various, 2)) + """</td>
                   <td>""" + str(round(rec.various_percent, 2)) + """</td>
                </tr>
                <tr style="background: #e9ecef;">
                   <td style="font-weight: bold;">""" + _('Direct Costs') + """</td>
                   <td>""" + str(round(rec.direct_costs, 2)) + """</td>
                   <td>""" + str(round(rec.direct_costs_percent, 2)) + """</td>
                </tr>
                <tr>
                    <td>""" + _('Indirect Costs') + """</td>
                    <td>""" + str(round(rec.indirect_costs, 2)) + """</td>
                    <td>""" + str(round(rec.indirect_costs_percent, 2)) + """</td>
                </tr>
                <tr style="background: #e9ecef;">
                    <td  style="font-weight: bold;">""" + _('Cost Price') + """</td>
                    <td>""" + str(round(rec.cost_price, 2)) + """</td>
                    <td>""" + str(round(rec.cost_price_percent, 2)) + """</td>
                </tr>
                <tr>
                    <td  style="font-weight: bold;">""" + _('Billing') + """</td>
                    <td>""" + str(round(rec.billing, 2)) + """</td>
                    <td>""" + str(round(rec.billing_percent, 2)) + """</td>
                </tr>
                <tr style="background: #e9ecef;">
                    <td style="font-weight: bold;">""" + _('Result') + """</td>
                    <td>""" + str(round(rec.result, 2)) + """</td>
                    <td>""" + str(round(rec.result_percent, 2)) + """</td>
                </tr>
                <tr class="blank_row" style="height: 30px !important; width: 100%;">
                   <td colspan="7"></td>
                </tr>

                <tr style="background: #e9ecef;">
                   <td>""" + _('Nbr of hours') + """</td>
                   <td>""" + str(round(rec.nb_hours, 2)) + """</td>
                   <td> - </td>
                </tr>
                <tr>
                    <td>""" + _('Price of hour') + """</td>
                    <td>""" + str(round(rec.hour_price, 2)) + """</td>
                    <td> - </td>
                </tr>
            </table>           
            """
