# -*- coding: utf-8 -*-
from odoo import http,_
FIELD_TRANS = {
        'name': _('Project Name'),
        'land_type':_('Land Type'),
        'location':_('Location'),
        'floor_area': _("Floor Area(m2)"),
        'plot_ratio':_('Plot Ratio'),
        'volume_area': _("Volume Area(m2)"),
        'residential_area': _('Residential Area(m2)'),
        'bussiness_area':_('Bussiness Area(m2)'),
        'office_area':_('Office Area(m2)'),
        'other_area':_('Other Area(m2)'), 
        'site_situation':_('Site Situation'), 
        'transfer_type':_('Transfer Type'),
        'transfer_price':_('Transfer Price(Yi Yuan)'),
        'voice_cost': _('Voice Cost(Yi Yuan)'),
        'floor_price':_('Floor Price(Yuan/m2)'),
        'saler_introduction':_('Saler Introduction'),
        'saler_core_requirement':_('Saler Core Requirement'),
        'agent_introduction':_('Agent Introduction'),
        'debt_situation':_('Debt Situation'),
        'estimate_sale_price':_('Estimate Sale Price(Yi Yuan)'),
        'product_value':_('Product Value'),
        'net_profit_rate':_('Net Profit Rate(%)'),
        'base_judgement':_('Base Judgement'),
        }

class SceLawsuit(http.Controller):
    pass

