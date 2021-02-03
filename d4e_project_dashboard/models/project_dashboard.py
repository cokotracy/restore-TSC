from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
import datetime
from datetime import datetime
from datetime import date


class Project(models.Model):
    _inherit = "project.project"

    selectable_fields = ['launch_workforce',
                         'launch_various','launch_direct_costs','launch_indirect_costs','launch_cost_price',
                         'launch_billing','launch_result','launch_hours','launch_hour_price'

                         'launch_workforce_percent',
                         'launch_various_percent', 'launch_direct_costs_percent',
                         'launch_indirect_costs_percent', 'launch_cost_price_percent','launch_billing_percent',
                         'launch_result_percent',

                         'month_workforce',
                         'month_various', 'month_direct_costs', 'month_indirect_costs', 'month_cost_price',
                         'month_billing', 'month_result', 'month_hours', 'month_hour_price',

                         'month_workforce_percent',
                         'month_various_percent', 'month_direct_costs_percent',
                         'month_indirect_costs_percent', 'month_cost_price_percent', 'month_billing_percent',
                         'month_result_percent','month_hours_percent',

                         'cum_workforce',
                         'cum_various', 'cum_direct_costs', 'cum_indirect_costs', 'cum_cost_price',
                         'cum_billing', 'cum_result', 'cum_hours', 'cum_hour_price'

                         'cum_workforce_percent',
                         'cum_various_percent', 'cum_direct_costs_percent',
                         'cum_indirect_costs_percent', 'cum_cost_price_percent', 'cum_billing_percent',
                         'cum_result_percent','cum_hours_percent',
                         ]

    name = fields.Char("Name", index=True, required=True, tracking=True, compute='_compute_name', default='/', store=True)


    # sale_order_ids = fields.One2many('sale.order', 'project_id', string='Quotations / Sales Orders')
    dashboard_table = fields.Html(string="Dashboard", compute='_compute_dashboard', translate=True)
    timesheet_lines = fields.One2many('account.analytic.line', 'project_id', 'Timesheet Lines',
                                      compute='_compute_timesheet_lines', store=False)

    target_hour_cost = fields.Float(string='Target hourly cost')
    total_cost = fields.Float(string='Total target cost', compute='_compute_total_cost')

    allow_billable = fields.Boolean("Bill from Tasks",default=True)
    invoices = fields.One2many('account.move', compute='compute_invoice_bills')
    bills = fields.One2many('account.move', compute='compute_invoice_bills')

    def compute_invoice_bills(self):
        for rec in self:
            rec.invoices = rec.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice')
            rec.bills = rec.invoice_ids.filtered(lambda inv: inv.type == 'in_invoice')

    def _get_project_types(self):
        types = self.env['project.type'].search([('company_id','=', self.env.company.id)])
        project_types = []
        for t in types:
            project_types.append((t.code, t.name))
        return project_types


    project_type = fields.Selection(_get_project_types, string='Project Type')
    project_name = fields.Char('Project name',required=True)
    price_per_hour = fields.Float('Price per hour')

    @api.depends('user_id','user_id.name','project_name','project_type')
    def _compute_name(self):
        for rec in self:
            responsable = ""
            resp_name = rec.user_id.name.split(' ')
            for i in range(0,len(resp_name)):
                ch = resp_name[i][0]
                responsable += ch
            if responsable and rec.project_name and rec.project_type:
                rec.name = responsable + ' - ' + rec.project_name + ' - ' + (rec.project_type.capitalize())
            else:
                rec.name = " "


    @api.onchange('project_type')
    def onchange_method(self):
        project_type = self.env['project.type'].search([('code','=',self.project_type)])
        self.price_per_hour = project_type.price

    def _compute_total_cost(self):
        for rec in self:
            total_time = 0
            for line in rec.timesheet_lines:
                total_time += line.unit_amount
            if rec.target_hour_cost !=0 and total_time != 0:
                rec.total_cost = rec.target_hour_cost * total_time
            else:
                rec.total_cost = 0


    def _compute_timesheet_lines(self):
        for rec in self:
            related_recordset = self.env['account.analytic.line'].search([('project_id', '=', rec.id)])
            rec.timesheet_lines = related_recordset

    # champs de la colonne lancement
    launch_workforce = fields.Float('Launch - Workforce', compute='_compute_launch_fields', store=True, readonly=False)
    launch_various = fields.Float('Launch - Various', compute='_compute_launch_fields', store=True, readonly=False)
    launch_direct_costs = fields.Float('Launch - Direct Costs', compute='_compute_launch_fields', store=True, readonly=False)
    launch_indirect_costs = fields.Float('Launch - Indirect Costs', compute='_compute_launch_fields', store=True, readonly=False)
    launch_cost_price = fields.Float('Launch - Cost Price', compute='_compute_launch_fields', store=True, readonly=False)
    launch_billing = fields.Float('Launch - Billing', compute='_compute_launch_fields', store=True, readonly=False)
    launch_result = fields.Float('Launch - Result', compute='_compute_launch_fields', store=True, readonly=False)
    launch_hours = fields.Float('Launch - Nb of Hours', compute='_compute_launch_fields', store=True, readonly=False)
    launch_hour_price = fields.Float('Launch - Price of hour', compute='_compute_launch_fields', store=True, readonly=False)

    # champs de la colonne % Lancement
    launch_workforce_percent = fields.Float(_('Launch - Workforce (%)'), digits=dp.get_precision('Discount'),
                                            compute='_compute_launch_fields_percent', store=True, readonly=False)
    launch_various_percent = fields.Float(_('Launch - Various (%)'), dp.get_precision('Discount'),
                                          compute='_compute_launch_fields_percent', store=True, readonly=False)
    launch_direct_costs_percent = fields.Float(_('Launch - Direct Costs (%)'), dp.get_precision('Discount'),
                                               compute='_compute_launch_fields_percent', store=True, readonly=False)
    launch_indirect_costs_percent = fields.Float(_('Launch - Indirect Costs (%)'), dp.get_precision('Discount'),
                                                 compute='_compute_launch_fields_percent', store=True, readonly=False)
    launch_cost_price_percent = fields.Float(_('Launch - Cost Price (%)'), dp.get_precision('Discount'),
                                             compute='_compute_launch_fields_percent', store=True, readonly=False)
    launch_billing_percent = fields.Float(_('Launch - Billing (%)'), dp.get_precision('Discount'),
                                          compute='_compute_launch_fields_percent', store=True, readonly=False)
    launch_result_percent = fields.Float(_('Launch - Result (%)'), dp.get_precision('Discount'),
                                         compute='_compute_launch_fields_percent', store=True, readonly=False)

    # champs de la colonne mois
    month_workforce = fields.Float(_('Month - Workforce'), compute='_compute_month_fields', store=True, readonly=False)
    month_various = fields.Float(_('Month - Various'), compute='_compute_month_fields', store=True, readonly=False)
    month_direct_costs = fields.Float(_('Month - Direct Costs'), compute='_compute_month_fields', store=True, readonly=False)
    month_indirect_costs = fields.Float(_('Month - Indirect Costs'), compute='_compute_month_fields', store=True, readonly=False)
    month_cost_price = fields.Float(_('Month - Cost Price'), compute='_compute_month_fields', store=True, readonly=False)
    month_billing = fields.Float(_('Month - Billing'), compute='_compute_month_fields', store=True, readonly=False)
    month_result = fields.Float(_('Month - Result'), compute='_compute_month_fields', store=True, readonly=False)
    month_hours = fields.Float(_('Month - Nb of Hours'), compute='_compute_month_fields', store=True, readonly=False)
    month_hour_price = fields.Float(_('Month - Price of Hour'), compute='_compute_month_fields', store=True, readonly=False)

    # champs de la colonne % mois
    month_workforce_percent = fields.Float(_('Month - Workforce (%)'), digits=dp.get_precision('Discount'),
                                           compute='_compute_month_fields_percent', store=True, readonly=False)
    month_various_percent = fields.Float(_('Month - Various (%)'), dp.get_precision('Discount'),
                                         compute='_compute_month_fields_percent', store=True, readonly=False)
    month_direct_costs_percent = fields.Float(_('Month - Direct Costs (%)'), dp.get_precision('Discount'),
                                              compute='_compute_month_fields_percent', store=True, readonly=False)
    month_indirect_costs_percent = fields.Float(_('Month - Indirect Costs (%)'), dp.get_precision('Discount'),
                                                compute='_compute_month_fields_percent', store=True, readonly=False)
    month_cost_price_percent = fields.Float(_('Month - Cost Price (%)'), dp.get_precision('Discount'),
                                            compute='_compute_month_fields_percent', store=True, readonly=False)
    month_billing_percent = fields.Float(_('Month - Billing (%)'), dp.get_precision('Discount'),
                                         compute='_compute_month_fields_percent', store=True, readonly=False)
    month_result_percent = fields.Float(_('Month - Result (%)'), dp.get_precision('Discount'),
                                        compute='_compute_month_fields_percent', store=True, readonly=False)
    month_hours_percent = fields.Float(_('Month - Nb of Hours (%)'), dp.get_precision('Discount'),
                                       compute='_compute_month_fields_percent', store=True, readonly=False)

    # champs de la colonne cumulé
    cum_workforce = fields.Float(_('Cumulated - Workforce'), compute='_compute_cum_fields', store=True, readonly=False)
    cum_various = fields.Float('Cumulated - Various', compute='_compute_cum_fields', store=True, readonly=False)
    cum_direct_costs = fields.Float('Cumulated - Direct Costs', compute='_compute_cum_fields', store=True, readonly=False)
    cum_indirect_costs = fields.Float('Cumulated - Indirect Costs', compute='_compute_cum_fields', store=True, readonly=False)
    cum_cost_price = fields.Float('Cumulated - Cost Price', compute='_compute_cum_fields', store=True, readonly=False)
    cum_billing = fields.Float('Cumulated - Billing', compute='_compute_cum_fields', store=True, readonly=False)
    cum_result = fields.Float('Cumulated - Result', compute='_compute_cum_fields', store=True, readonly=False)
    cum_hours = fields.Float('Cumulated - Result', compute='_compute_cum_fields', store=True, readonly=False)
    cum_hour_price = fields.Float('Cumulated - Nb of Hours', compute='_compute_cum_fields', store=True, readonly=False)

    # champs de la colonne % cumulé
    cum_workforce_percent = fields.Float(_('Cumulated - Workforce (%)'), digits=dp.get_precision('Discount'),
                                         compute='_compute_cum_fields_percent', store=True, readonly=False)
    cum_various_percent = fields.Float(_('Cumulated - Various (%)'), dp.get_precision('Discount'),
                                       compute='_compute_cum_fields_percent', store=True, readonly=False)
    cum_direct_costs_percent = fields.Float(_('Cumulated - Direct Costs (%)'), dp.get_precision('Discount'),
                                            compute='_compute_cum_fields_percent', store=True, readonly=False)
    cum_indirect_costs_percent = fields.Float(_('Cumulated - Indirect Costs (%)'), dp.get_precision('Discount'),
                                              compute='_compute_cum_fields_percent', store=True, readonly=False)
    cum_cost_price_percent = fields.Float(_('Cumulated - Cost Price (%)'), dp.get_precision('Discount'),
                                          compute='_compute_cum_fields_percent', store=True, readonly=False)
    cum_billing_percent = fields.Float(_('Cumulated - Billing (%)'), dp.get_precision('Discount'),
                                       compute='_compute_cum_fields_percent', store=True, readonly=False)
    cum_result_percent = fields.Float(_('Cumulated - Result (%)'), dp.get_precision('Discount'),
                                      compute='_compute_cum_fields_percent', store=True, readonly=False)
    cum_hours_percent = fields.Float(_('Cumulated - Nb of Hours (%)'), dp.get_precision('Discount'),
                                     compute='_compute_cum_fields_percent', store=True, readonly=False)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(Project, self).fields_get(allfields, attributes=attributes)
        fields_to_hide = set(self._fields.keys()) - set(self.selectable_fields)
        for field in fields_to_hide:
            if field in res.keys():
                res[field]['selectable'] = False
        return res

    def _get_ind_cost_prod_id(self):
        return self.env['ir.config_parameter'].sudo().get_param('project_dashboard.indirect_costs_product_id') or False

    def _get_benef_prod_id(self):
        return self.env['ir.config_parameter'].sudo().get_param('project_dashboard.benefice_product_id') or False

    def _get_mo_categ_id(self):
        return self.env['ir.config_parameter'].sudo().get_param('project_dashboard.workforce_category_id') or False

    def _init_launch_fields(self):
        """ initialiser les champs lancement """
        self.launch_workforce = 0
        self.launch_various = 0
        self.launch_direct_costs = 0
        self.launch_indirect_costs = 0
        self.launch_cost_price = 0
        self.launch_billing = 0
        self.launch_result = 0
        self.launch_hours = 0
        self.launch_hour_price = 0

    def _init_launch_percent_fields(self):
        """ initialiser les champs lancement (%)"""
        self.launch_workforce_percent = 0
        self.launch_various_percent = 0
        self.launch_direct_costs_percent = 0
        self.launch_indirect_costs_percent = 0
        self.launch_cost_price_percent = 0
        self.launch_billing_percent = 0
        self.launch_result_percent = 0

    def _init_month_fields(self):
        """ initialiser les champs mois """
        self.month_workforce = 0
        self.month_various = 0
        self.month_direct_costs = 0
        self.month_indirect_costs = 0
        self.month_cost_price = 0
        self.month_billing = 0
        self.month_result = 0
        self.month_hours = 0
        self.month_hour_price = 0

    def _init_month_percent_fields(self):
        """ initialiser les champs Mois (%) """
        self.month_workforce_percent = 0
        self.month_various_percent = 0
        self.month_direct_costs_percent = 0
        self.month_indirect_costs_percent = 0
        self.month_cost_price_percent = 0
        self.month_billing_percent = 0
        self.month_result_percent = 0
        self.month_hours_percent = 0

    def _init_cum_fields(self):
        """ initialiser les champs cumulé """
        self.cum_workforce = 0
        self.cum_various = 0
        self.cum_direct_costs = 0
        self.cum_indirect_costs = 0
        self.cum_cost_price = 0
        self.cum_billing = 0
        self.cum_result = 0
        self.cum_hours = 0
        self.cum_hour_price = 0

    def _init_cum_percent_fields(self):
        """ initialiser les champs Cumulé (%)"""
        self.cum_workforce_percent = 0
        self.cum_various_percent = 0
        self.cum_direct_costs_percent = 0
        self.cum_indirect_costs_percent = 0
        self.cum_cost_price_percent = 0
        self.cum_billing_percent = 0
        self.cum_result_percent = 0
        self.cum_hours_percent = 0

    @api.depends(
                'timesheet_lines', 'timesheet_lines.unit_amount',
                 'timesheet_lines.employee_id', 'timesheet_lines.employee_id.timesheet_cost',
                 'sale_order_ids',
                 'sale_order_ids.state',
                 'sale_order_ids.order_line',
                 'sale_order_ids.order_line.product_id',
                 'sale_order_ids.order_line.product_id.categ_id',
                 'sale_order_ids.order_line.price_subtotal')
    def _compute_launch_fields(self):
        self._init_launch_fields()
        for rec in self:
            for so in rec.sale_order_ids:
                if so.state == 'sale' or so.state == 'done':

                    for line in so.order_line:
                        is_benefice = (int(line.product_id.id) == int(self._get_benef_prod_id()))
                        is_mo = (int(line.product_id.categ_id.id) == int(self._get_mo_categ_id()))
                        is_ind_cost = (int(line.product_id.id) == int(self._get_ind_cost_prod_id()))

                        # calcule du champ MO
                        if is_mo:
                            rec.launch_workforce += line.price_subtotal
                            # calcule du champ nb heures
                            rec.launch_hours += line.product_uom_qty


                        # calcule du champ frais généraux
                        elif is_ind_cost:
                            rec.launch_indirect_costs += line.price_subtotal


                        # calcule du champ divers
                        elif not is_benefice:
                            rec.launch_various += line.price_subtotal



                    # calcul du champ couts directes
                    rec.launch_direct_costs = rec.launch_workforce + rec.launch_various

                    # calcule du champ facturation
                    rec.launch_billing += so.amount_untaxed

                    # calcule du champ prix de revenue
                    rec.launch_cost_price = rec.launch_direct_costs + rec.launch_indirect_costs

                    # calcule du champ Résultat
                    rec.launch_result = rec.launch_billing - rec.launch_cost_price

                    # calcule du champ prix de l’heure
                    if rec.launch_hours != 0:
                        rec.launch_hour_price = rec.launch_billing / rec.launch_hours


    @api.depends('timesheet_lines', 'timesheet_lines.unit_amount',
                 'timesheet_lines.employee_id', 'timesheet_lines.employee_id.timesheet_cost',
                 'sale_order_ids',
                 'sale_order_ids.state',
                 'sale_order_ids.order_line',
                 'sale_order_ids.order_line.product_id',
                 'sale_order_ids.order_line.product_id.categ_id',
                 'sale_order_ids.order_line.price_subtotal',
                 'launch_billing', 'launch_workforce',
                 'launch_various', 'launch_direct_costs', 'launch_indirect_costs', 'launch_cost_price',
                 'launch_result', )
    def _compute_launch_fields_percent(self):
        self._init_launch_percent_fields()
        for rec in self:
            billing = rec.launch_billing
            if billing != 0:
                # pourcentage MO
                rec.launch_workforce_percent = (rec.launch_workforce * 100) / billing
                # pourcentage divers
                rec.launch_various_percent = (rec.launch_various * 100) / billing
                # pourcentage couts directes
                rec.launch_direct_costs_percent = (rec.launch_direct_costs * 100) / billing
                # pourcentage Frais généraux
                rec.launch_indirect_costs_percent = (rec.launch_indirect_costs * 100) / billing
                # pourcentage prix de revenues
                rec.launch_cost_price_percent = (rec.launch_cost_price * 100) / billing
                # pourcentage Facturation
                rec.launch_billing_percent = (rec.launch_billing * 100) / billing
                # pourcentage résultat
                rec.launch_result_percent = (rec.launch_result * 100) / billing

    @api.depends('timesheet_lines', 'timesheet_lines.unit_amount',
                 'timesheet_lines.employee_id', 'timesheet_lines.employee_id.timesheet_cost',
                 'timesheet_lines.date',
                 'sale_order_ids',
                 'sale_order_ids.state',
                 'sale_order_ids.order_line',
                 'invoice_ids',
                 'invoice_ids.invoice_date',
                 'invoice_ids.invoice_line_ids',
                 'invoice_ids.amount_untaxed',
                 'invoice_ids.invoice_line_ids.product_id',
                 'invoice_ids.invoice_line_ids.product_id.categ_id',
                 'invoice_ids.invoice_line_ids.price_subtotal')
    def _compute_month_fields(self):
        self._init_month_fields()
        for rec in self:
            # for so in rec.sale_order_ids:
            for inv in rec.invoice_ids:
                if inv.invoice_date:
                    current_month = datetime.strptime(str(date.today()), '%Y-%m-%d').strftime('%m')
                    invoice_month = datetime.strptime(str(inv.invoice_date), '%Y-%m-%d').strftime('%m')
                    if inv.state == 'posted' and invoice_month == current_month:
                        for line in inv.invoice_line_ids:
                            is_benefice = (int(line.product_id.id) == int(self._get_benef_prod_id()))
                            is_mo = (int(line.product_id.categ_id.id) == int(self._get_mo_categ_id()))
                            is_ind_cost = (int(line.product_id.id) == int(self._get_ind_cost_prod_id()))


                            # calcule du champ divers
                            if not is_benefice and not is_mo and not is_ind_cost:
                                rec.month_various += line.price_subtotal

                        # calcule du champ facturation
                        rec.month_billing += inv.amount_untaxed

            for line in rec.timesheet_lines:
                current_month = datetime.strptime(str(date.today()), '%Y-%m-%d').strftime('%m')
                line_month = datetime.strptime(str(line.date), '%Y-%m-%d').strftime('%m')
                if line_month == current_month:
                    # calcule du champ nb heures
                    rec.month_hours += line.unit_amount
                    # calcule du champ MO
                    rec.month_workforce += line.unit_amount * line.employee_id.timesheet_cost

                    # calcule du champ prix de l’heure
                    if rec.month_hours != 0:
                        rec.month_hour_price = rec.month_billing / rec.month_hours

            rec.month_indirect_costs = rec.month_workforce * 0.25 / 0.65
            rec.month_direct_costs = rec.month_workforce + rec.month_various
            # calcule du champ prix de revenue
            rec.month_cost_price = rec.month_direct_costs + rec.month_indirect_costs
            # calcule du champ Résultat
            rec.month_result = rec.month_billing - rec.month_cost_price

    @api.depends('timesheet_lines', 'timesheet_lines.unit_amount',
                 'timesheet_lines.employee_id', 'timesheet_lines.employee_id.timesheet_cost',
                 'timesheet_lines.date',
                 'sale_order_ids',
                 'sale_order_ids.state',
                 'sale_order_ids.order_line',
                 'invoice_ids',
                 'invoice_ids.invoice_date',
                 'invoice_ids.invoice_line_ids',
                 'invoice_ids.amount_untaxed',
                 'invoice_ids.invoice_line_ids.product_id',
                 'invoice_ids.invoice_line_ids.product_id.categ_id',
                 'invoice_ids.invoice_line_ids.price_subtotal',
                 'month_billing', 'launch_hours', 'month_hours', 'month_workforce',
                 'month_various', 'month_direct_costs', 'month_indirect_costs', 'month_cost_price',
                 'month_billing', 'month_result')
    def _compute_month_fields_percent(self):
        self._init_month_percent_fields()
        for rec in self:
            billing = rec.month_billing
            hours = rec.launch_hours
            if hours != 0:
                # pourcentage nb d'heures
                rec.month_hours_percent = (rec.month_hours * 100) / hours
            if billing != 0:
                # pourcentage MO
                rec.month_workforce_percent = (rec.month_workforce * 100) / billing
                # pourcentage divers
                rec.month_various_percent = (rec.month_various * 100) / billing
                # pourcentage couts directes
                rec.month_direct_costs_percent = (rec.month_direct_costs * 100) / billing
                # pourcentage Frais généraux
                rec.month_indirect_costs_percent = (rec.month_indirect_costs * 100) / billing
                # pourcentage prix de revenues
                rec.month_cost_price_percent = (rec.month_cost_price * 100) / billing
                # pourcentage Facturation
                rec.month_billing_percent = (rec.month_billing * 100) / billing
                # pourcentage résultat
                rec.month_result_percent = (rec.month_result * 100) / billing

    @api.depends('timesheet_lines', 'timesheet_lines.unit_amount',
                 'timesheet_lines.employee_id',
                 'timesheet_lines.employee_id.timesheet_cost',
                 'sale_order_ids',
                 'sale_order_ids.state',
                 'sale_order_ids.order_line',
                 'invoice_ids',
                 'invoice_ids.state',
                 'invoice_ids.invoice_line_ids',
                 'invoice_ids.amount_untaxed',
                 'invoice_ids.invoice_line_ids.product_id',
                 'invoice_ids.invoice_line_ids.product_id.categ_id',
                 'invoice_ids.invoice_line_ids.price_subtotal')
    def _compute_cum_fields(self):
        self._init_cum_fields()
        for rec in self:

            for inv in rec.invoice_ids:
                if inv.state == 'posted':
                    for line in inv.invoice_line_ids:
                        is_benefice = (int(line.product_id.id) == int(self._get_benef_prod_id()))
                        is_mo = (int(line.product_id.categ_id.id) == int(self._get_mo_categ_id()))
                        is_ind_cost = (int(line.product_id.id) == int(self._get_ind_cost_prod_id()))

                        # calcule du champ divers
                        if not is_benefice and not is_mo and not is_ind_cost:
                            rec.cum_various += line.price_subtotal
                    # calcule du champ facturation
                    rec.cum_billing += inv.amount_untaxed

            for line in rec.timesheet_lines:

                # calcule du champ nb heures
                rec.cum_hours += line.unit_amount
                # calcule du champ MO
                rec.cum_workforce += line.unit_amount * line.employee_id.timesheet_cost

                # calcule du champ prix de l’heure
                if rec.cum_hours != 0:
                    rec.cum_hour_price = rec.cum_billing / rec.cum_hours

            rec.cum_indirect_costs = rec.cum_workforce * 0.25 / 0.65
            # calcul du champ couts directes
            rec.cum_direct_costs = rec.cum_workforce + rec.cum_various
            # calcule du champ prix de revenue
            rec.cum_cost_price = rec.cum_direct_costs + rec.cum_indirect_costs
            # calcule du champ Résultat
            rec.cum_result = rec.cum_billing - rec.cum_cost_price

    @api.depends('timesheet_lines', 'timesheet_lines.unit_amount',
                 'timesheet_lines.employee_id',
                 'timesheet_lines.employee_id.timesheet_cost',
                 'sale_order_ids',
                 'sale_order_ids.state',
                 'sale_order_ids.order_line',
                 'invoice_ids',
                 'invoice_ids.state',
                 'invoice_ids.invoice_line_ids',
                 'invoice_ids.amount_untaxed',
                 'invoice_ids.invoice_line_ids.product_id',
                 'invoice_ids.invoice_line_ids.product_id.categ_id',
                 'invoice_ids.invoice_line_ids.price_subtotal',
                 'cum_billing', 'launch_hours', 'cum_hours', 'cum_workforce',
                 'cum_various', 'cum_direct_costs', 'cum_indirect_costs', 'cum_cost_price', 'cum_result')
    def _compute_cum_fields_percent(self):
        self._init_cum_percent_fields()
        for rec in self:
            billing = rec.cum_billing
            hours = rec.launch_hours

            if hours != 0:
                # pourcentage nb d'heures
                rec.cum_hours_percent = (rec.cum_hours * 100) / hours

            if billing != 0:
                # pourcentage MO
                rec.cum_workforce_percent = (rec.cum_workforce * 100) / billing
                # pourcentage divers
                rec.cum_various_percent = (rec.cum_various * 100) / billing
                # pourcentage couts directes
                rec.cum_direct_costs_percent = (rec.cum_direct_costs * 100) / billing
                # pourcentage Frais généraux
                rec.cum_indirect_costs_percent = (rec.cum_indirect_costs * 100) / billing
                # pourcentage prix de revenues
                rec.cum_cost_price_percent = (rec.cum_cost_price * 100) / billing
                # pourcentage Facturation
                rec.cum_billing_percent = (rec.cum_billing * 100) / billing
                # pourcentage résultat
                rec.cum_result_percent = (rec.cum_result * 100) / billing

    def _compute_dashboard(self):
        for rec in self:
            rec.dashboard_table = """
                            <table style="width: 100%;">
                                <tr>
                                  <th style="width:25%"> </th>
                                  <th style="width:10%">""" + _('Launch') + """</th>
                                  <th style="width:20%">%</th>
                                  <th style="width:10%">""" + _('Month') + """</th>
                                  <th style="width:20%">%</th>
                                  <th>""" + _('Cumulative') + """</th>
                                  <th>%</th>
                                </tr>
                                <tr style="background: #e9ecef;">
                                  <td>""" + _('Workforce') + """</td>
                                  <td>""" + str(round(self.launch_workforce, 2)) + """</td>
                                  <td>""" + str(round(self.launch_workforce_percent, 2)) + """</td>
                                  <td>""" + str(round(self.month_workforce, 2)) + """</td>
                                  <td>""" + str(round(self.month_workforce_percent, 2)) + """</td>
                                  <td>""" + str(round(self.cum_workforce, 2)) + """</td>
                                  <td>""" + str(round(self.cum_workforce_percent, 2)) + """</td>
                                </tr>
                               <tr>
                                 <td>""" + _('Various') + """</td>
                                 <td>""" + str(round(self.launch_various, 2)) + """</td>
                                 <td>""" + str(round(self.launch_various_percent, 2)) + """</td>
                                 <td>""" + str(round(self.month_various, 2)) + """</td>
                                 <td>""" + str(round(self.month_various_percent, 2)) + """</td>
                                 <td>""" + str(round(self.cum_various, 2)) + """</td>
                                 <td>""" + str(round(self.cum_various_percent, 2)) + """</td>
                               </tr>
                               <tr style="background: #e9ecef;">
                                 <td style="font-weight: bold;">""" + _('Direct Costs') + """</td>
                                 <td>""" + str(round(self.launch_direct_costs, 2)) + """</td>
                                 <td>""" + str(round(self.launch_direct_costs_percent, 2)) + """</td>
                                 <td>""" + str(round(self.month_direct_costs, 2)) + """</td>
                                 <td>""" + str(round(self.month_direct_costs_percent, 2)) + """</td>
                                 <td>""" + str(round(self.cum_direct_costs, 2)) + """</td>
                                 <td>""" + str(round(self.cum_direct_costs_percent, 2)) + """</td>
                               </tr>
                               <tr>
                                 <td>""" + _('Indirect Costs') + """</td>
                                 <td>""" + str(round(self.launch_indirect_costs, 2)) + """</td>
                                 <td>""" + str(round(self.launch_indirect_costs_percent, 2)) + """</td>
                                 <td>""" + str(round(self.month_indirect_costs, 2)) + """</td>
                                 <td>""" + str(round(self.month_indirect_costs_percent, 2)) + """</td>
                                 <td>""" + str(round(self.cum_indirect_costs, 2)) + """</td>
                                 <td>""" + str(round(self.cum_indirect_costs_percent, 2)) + """</td>
                               </tr>
                               <tr style="background: #e9ecef;">
                                  <td  style="font-weight: bold;">""" + _('Cost Price') + """</td>
                                  <td>""" + str(round(self.launch_cost_price, 2)) + """</td>
                                  <td>""" + str(round(self.launch_cost_price_percent, 2)) + """</td>
                                  <td>""" + str(round(self.month_cost_price, 2)) + """</td>
                                  <td>""" + str(round(self.month_cost_price_percent, 2)) + """</td>
                                  <td>""" + str(round(self.cum_cost_price, 2)) + """</td>
                                  <td>""" + str(round(self.cum_cost_price_percent, 2)) + """</td>
                               </tr>
                               <tr>
                                 <td  style="font-weight: bold;">""" + _('Billing') + """</td>
                                 <td>""" + str(round(self.launch_billing, 2)) + """</td>
                                 <td>""" + str(round(self.launch_billing_percent, 2)) + """</td>
                                 <td>""" + str(round(self.month_billing, 2)) + """</td>
                                 <td>""" + str(round(self.month_billing_percent, 2)) + """</td>
                                 <td>""" + str(round(self.cum_billing, 2)) + """</td>
                                 <td>""" + str(round(self.cum_billing_percent, 2)) + """</td>
                               </tr>
                               <tr style="background: #e9ecef;">
                                  <td style="font-weight: bold;">""" + _('Result') + """</td>
                                  <td>""" + str(round(self.launch_result, 2)) + """</td>
                                  <td>""" + str(round(self.launch_result_percent, 2)) + """</td>
                                  <td>""" + str(round(self.month_result, 2)) + """</td>
                                  <td>""" + str(round(self.month_result_percent, 2)) + """</td>
                                  <td>""" + str(round(self.cum_result, 2)) + """</td>
                                  <td>""" + str(round(self.cum_result_percent, 2)) + """</td>
                               </tr>
                               <tr class="blank_row" style="height: 30px !important; width: 100%;">
                                   <td colspan="7"></td>
                               </tr>

                              <tr style="background: #e9ecef;">
                                 <td>""" + _('Nbr of hours') + """</td>
                                 <td>""" + str(round(self.launch_hours, 2)) + """</td>
                                 <td> - </td>
                                 <td>""" + str(round(self.month_hours, 2)) + """</td>
                                 <td>""" + str(round(self.month_hours_percent, 2)) + """</td>
                                 <td>""" + str(round(self.cum_hours, 2)) + """</td>
                                 <td>""" + str(round(self.cum_hours_percent, 2)) + """</td>
                               </tr>
                               <tr>
                                 <td>""" + _('Price of hour') + """</td>
                                 <td>""" + str(round(self.launch_hour_price, 2)) + """</td>
                                 <td> - </td>
                                 <td>""" + str(round(self.month_hour_price, 2)) + """</td>
                                 <td> - </td>
                                 <td>""" + str(round(self.cum_hour_price, 2)) + """</td>
                                 <td> - </td>
                               </tr>
                            </table>"""

class ProjectType(models.Model):
    _name = 'project.type'

    code = fields.Char('Code')
    name = fields.Char('Name')
    price = fields.Float('Price per hour')
    company_id = fields.Many2one('res.company',string='Company',
                                 default=lambda self: self.env.company, required=True)
