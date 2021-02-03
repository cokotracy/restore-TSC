from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def affect_default_tasks(self):
        model_project = self.env['project.project']
        model_project_task = self.env['project.task']
        projects = model_project.search([])
        for project in projects:
            has_default_tasks = model_project_task.search([('is_default','=',True),('project_id','=',project.id)])
            if has_default_tasks and project.use_default_tasks == False:
                project.use_default_tasks = True
            elif not has_default_tasks and project.use_default_tasks == False:
                project.use_default_tasks = True
                project.create_default_tasks(project_id=project)
            elif not has_default_tasks and project.use_default_tasks == True:
                project.create_default_tasks(project_id=project)

