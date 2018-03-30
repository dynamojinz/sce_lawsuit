# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Subcompany(models.Model):
    _name = 'sce_lawsuit.subcompany'

    name = fields.Char(required=True)
    user_ids = fields.Many2many('res.users')


