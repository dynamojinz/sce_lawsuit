# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Subcompany(models.Model):
    _name = 'sce_landinfo.subcompany'

    name = fields.Char(required=True)
    land_manager_id = fields.Many2one('res.users')
    general_manager_id = fields.Many2one('res.users')
    user_ids = fields.Many2many('res.users')


