
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    indirect_costs_product_id = fields.Many2one('product.product',
                                                default_model='project.project',
                                                string='Indirect Costs Product')

    benefice_product_id = fields.Many2one('product.product',
                                          default_model='project.project',
                                          string='Benefice Product')

    workforce_category_id = fields.Many2one('product.category',
                                                        default_model='project.project',
                                                        string='Workforce Category')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            indirect_costs_product_id = int(self.env['ir.config_parameter'].sudo().get_param('project_dashboard.indirect_costs_product_id')),
            benefice_product_id = int(self.env['ir.config_parameter'].sudo().get_param('project_dashboard.benefice_product_id')),
            workforce_category_id = int(self.env['ir.config_parameter'].sudo().get_param('project_dashboard.workforce_category_id')),
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        field1 = self.indirect_costs_product_id and self.indirect_costs_product_id.id or False
        field2 = self.benefice_product_id and self.benefice_product_id.id or False
        field3 = self.workforce_category_id and self.workforce_category_id.id or False

        param.set_param('project_dashboard.indirect_costs_product_id', field1)
        param.set_param('project_dashboard.benefice_product_id', field2)
        param.set_param('project_dashboard.workforce_category_id', field3)

    def recompute_stored_values(self):
        model = self.env['project.project']
        projects = model.search([])
        for project in projects:
            project._compute_launch_fields()
            project._compute_launch_fields_percent()
            project._compute_month_fields()
            project._compute_month_fields_percent()
            project._compute_cum_fields()
            project._compute_cum_fields_percent()

