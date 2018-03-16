# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LandUser(models.Model):
    _inherit='res.users'

    subcompany_ids = fields.Many2many('sce_landinfo.subcompany')
    

