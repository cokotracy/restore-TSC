# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = 'account.move'

    def copy(self,default=None):
        default = dict(default or {})
        default['ref'] = self.ref
        default['x_studio_titre'] = self.x_studio_titre

        return super(Invoice, self).copy(default)
