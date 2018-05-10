# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LandUser(models.Model):
    _inherit='res.users'

    lawsuit_subcompany_ids = fields.Many2many('sce_lawsuit.subcompany')
    

