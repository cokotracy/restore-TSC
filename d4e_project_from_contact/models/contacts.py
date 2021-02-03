from odoo import models, fields, api, _


class Contact(models.Model):
    _inherit = 'res.partner'

    project_ids = fields.One2many('project.project', 'partner_id','Projects')
    project_count = fields.Integer('Projects', compute='_compute_project_count')

    def _compute_project_count(self):
        for rec in self:
            rec.project_count = len(rec.project_ids)

    def add_project(self):
        ctx = dict(self.env.context, default_partner_id=self.id)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Project'),
            'res_model': 'project.project',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx
        }

    def action_open_projects(self):
        self.ensure_one()
        projects = self.env['project.project'].search([('partner_id', '=', self.id)])

        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            'view_mode': 'tree,form',
            "views": [[False, "tree"], [False, "form"]],
            "domain": [("id", "in", projects.ids)],
            "context": {'default_partner_id': self.id},
            "name": _("Projects"),
        }