# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import _
import datetime


# CHECKED_FIELDS = [ 'floor_area', 'plot_ratio', 'volume_area', 'residential_area', 'bussiness_area',
                    # 'office_area', 'other_area', 'site_situation', 'transfer_price',
                    # 'voice_cost', 'floor_price', 'estimate_sale_price', 'saler_introduction',
                    # 'saler_core_requirement', 'agent_introduction', 'debt_situation',
                    # 'product_value', 'net_profit_rate', 'base_judgement']

class Lawsuit(models.Model):
    _name = 'sce_lawsuit.lawsuit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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

    # 案件名称
    name = fields.Char(required=True)
    # 项目名称(涉诉项目）:
    project_name = fields.Char()
    # 区域
    region = fields.Char(required=True)
    # 案由
    cause = fields.Text(required=True)
    # 阶段
    state = fields.Selection( selection=[
            # ('mediation','Mediation'),                 # 调解
            ('arbitration','Arbitration'),             # 仲裁
            ('first_instance','First Instance'),       # 一审
            ('second_instance','Second Instance'),     # 二审
            ('enforcement','Enforcement'),             # 执行
        ],required=True)

    # 通知相关
    last_notify_date = fields.Date(default=fields.Date.today())

    ### 仲裁阶段 ###
    # 经办人
    arbi_operator = fields.Char('Operator', required=True)
    # 申请人
    arbi_claimant = fields.Char('Claimant', required=True)
    # 被申请人
    arbi_respondent = fields.Char('Respondent', required=True)
    # 仲裁请求
    arbi_claim = fields.Text('Arbitration claim', required=True)
    # 立案时间
    arbi_regist_date = fields.Date('Registration date', required=True)
    # 首次开庭时间
    arbi_open_date = fields.Date('Frist opening date', resquired=True)
    # 是否结案
    arbi_is_settled = fields.Boolean('Is settled', required=True)
    # 仲裁进展/结果
    arbi_result = fields.Text('Arbitration result', required=True)
    # 是否需申请执行
    arbi_need_enforcement = fields.Boolean('Need enforcement?')
    # 下次跟踪时间
    arbi_next_update_date = fields.Date()


    # @api.model
    # def process_update_notify(self):
        # # print('notify')
        # filters = ['&',
                # ('state','=','confirmed'),
                # ('next_update_date', '<=', fields.Datetime.context_timestamp(self,datetime.datetime.now())),
                # ('last_notify_date', '<', fields.Date.today()),
                # ('is_default_version', '=', True),
                # ('follow_up_status', '=', 'following'),
                # ]
        # results = self.sudo().search(filters)
        # # print(results)
        # # print(fields.Datetime.context_timestamp(self,datetime.datetime.now()))
        # for result in results:
            # mail = self.env['mail.thread'].with_context({'safe':True}).message_post(
                    # body = _("Your responsible land need to be updated:<br/>Name: %s<br/>Update Date: %s") % (result.name, result.next_update_date),
                    # subject = _('Land info update notification.'),
                    # partner_ids = [result.response_user_id.partner_id.id,],
                    # )
            # mail.notification_ids.sudo().write({'is_read':False})
            # # Send wechat message
            # wechat_message = _("Your responsible land need to be updated:\nName: %s\nUpdate Date: %s") % (result.name, result.next_update_date),
            # if isinstance(wechat_message, tuple):
                # wechat_message = wechat_message[0]
            # self.send_wechat_message(result.response_user_id, wechat_message)
            # # Redirect 
            # result.last_notify_date = fields.Date.today()

    # def send_wechat_message(self, user, message):
        # wechat = self.env['sce_wechat.wechat'].sudo().search([('is_master','=',True)])
        # logins = user.login.split('@')
        # if wechat and logins[-1]=='sce-re.com':
            # wechat.send_message(logins[0], message)
            # wechat.send_message('JinZan', message)

