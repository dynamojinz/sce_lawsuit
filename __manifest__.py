# -*- coding: utf-8 -*-
{
    'name': "Sce Lawsuit Management",

    'summary': """
        Designed for SCE, to manage lawsuits information.
        As well as update tracking, listing, ranging, and so on.""",

    'description': """
        Designed for SCE, to manage lawsuits information.
        As well as update tracking, listing, ranging, and so on.""",

    'author': "Jin Zan",
    'website': "http://www.sce-re.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sce_sso','sce_wechat'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/lawsuit_views.xml',
        'views/lawsuit_actions.xml',
        'views/menus.xml',
        # 'views/templates.xml',
        # 'views/mail_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable' : True,
    'application' : True,
}
