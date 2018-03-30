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

    # 负责人
    response_user_id = fields.Many2one('res.users', default=lambda self:self.env.user, readonly=True)

    ### 仲裁阶段 ###
    # 经办人
    arbi_operator = fields.Char('Operator', states={'arbitration':[('required',True)]})
    # 申请人
    arbi_claimant = fields.Char('Arbitration claimant', states={'arbitration':[('required',True)]})
    # 被申请人
    arbi_respondent = fields.Char('Arbitration respondent', states={'arbitration':[('required',True)]})
    # 仲裁请求
    arbi_claim = fields.Text('Arbitration claim', states={'arbitration':[('required',True)]})
    # 立案时间
    arbi_regist_date = fields.Date('Registration date', states={'arbitration':[('required',True)]})
    # 首次开庭时间
    arbi_open_date = fields.Date('Frist opening date', resquired=True)
    # 是否结案
    arbi_is_settled = fields.Boolean('Is settled', states={'arbitration':[('required',True)]})
    # 仲裁进展/结果
    arbi_result = fields.Text('Arbitration progress/results', states={'arbitration':[('required',True)]})
    # 是否需申请执行
    arbi_need_enforcement = fields.Boolean('Need enforcement?')
    # 下次跟踪时间
    arbi_next_update_date = fields.Date('Next update date')
    # 结案时间
    arbi_settled_date = fields.Date('Settled date')
    # 其他信息
    arbi_other_info = fields.Text('Other info')


    ### 一审阶段 ###
    # 经办人
    firs_operator = fields.Char('Operator', states={'first_instance':[('required',True)]})
    # 原告
    firs_claimant = fields.Char('Claimant', states={'first_instance':[('required',True)]})
    # 被告
    firs_respondent = fields.Char('Respondent', states={'first_instance':[('required',True)]})
    # 诉讼请求
    firs_claim = fields.Text('Claim', states={'first_instance':[('required',True)]})
    # 立案时间
    firs_regist_date = fields.Date('Registration date', states={'first_instance':[('required',True)]})
    # 首次开庭时间
    firs_open_date = fields.Date('Frist opening date', resquired=True)
    # 是否结案
    firs_is_settled = fields.Boolean('Is settled', states={'first_instance':[('required',True)]})
    # 诉讼进展/结果
    firs_result = fields.Text('Litigation progress/results', states={'first_instance':[('required',True)]})
    # 是否需申请执行
    firs_need_enforcement = fields.Boolean('Need enforcement?')
    # 下次跟踪时间
    firs_next_update_date = fields.Date('Next update date')
    # 结案时间
    firs_settled_date = fields.Date('Settled date')
    # 其他信息
    firs_other_info = fields.Text('Other info')

    ### 二审阶段 ###
    # 经办人
    seco_operator = fields.Char('Operator', states={'second_instance':[('required',True)]})
    # 上诉人 
    seco_claimant = fields.Char('Appellant', states={'second_instance':[('required',True)]})
    # 被上诉人
    seco_respondent = fields.Char('Appellee', states={'second_instance':[('required',True)]})
    # 上诉请求
    seco_claim = fields.Text('Appeals request', states={'second_instance':[('required',True)]})
    # 立案时间
    seco_regist_date = fields.Date('Registration date', states={'second_instance':[('required',True)]})
    # 首次开庭时间
    seco_open_date = fields.Date('Frist opening date', resquired=True)
    # 是否结案
    seco_is_settled = fields.Boolean('Is settled', states={'second_instance':[('required',True)]})
    # 诉讼进展/结果
    seco_result = fields.Text('Litigation progress/results', states={'second_instance':[('required',True)]})
    # 是否需申请执行
    seco_need_enforcement = fields.Boolean('Need enforcement?')
    # 下次跟踪时间
    seco_next_update_date = fields.Date('Next update date')
    # 结案时间
    seco_settled_date = fields.Date('Settled date')
    # 其他信息
    seco_other_info = fields.Text('Other info')

    ### 执行阶段 ###
    # 经办人
    enfo_operator = fields.Char('Operator', states={'enforcement':[('required',True)]})
    # 申请执行人 
    enfo_claimant = fields.Char('Claimant', states={'enforcement':[('required',True)]})
    # 被执行人 
    enfo_respondent = fields.Char('Respondent', states={'enforcement':[('required',True)]})
    # 执行请求
    enfo_claim = fields.Text('Claim', states={'enforcement':[('required',True)]})
    # # 立案时间
    # enfo_regist_date = fields.Date('Registration date', states={'enforcement':[('required',True)]})
    # # 首次开庭时间
    # enfo_open_date = fields.Date('Frist opening date', resquired=True)
    # 申请执行时间
    enfo_apply_date = fields.Date('Application enforcement date')
    # 是否结案
    enfo_is_settled = fields.Boolean('Is settled', states={'enforcement':[('required',True)]})
    # 执行进展/结果
    enfo_result = fields.Text('Enforcement progress/results', states={'enforcement':[('required',True)]})
    # 执行标的(金额)
    enfo_subject = fields.Char('Enforcement subject(amount of money)')
    # # 是否需申请执行
    # enfo_need_enforcement = fields.Boolean('Need enforcement?')
    # 下次跟踪时间
    enfo_next_update_date = fields.Date('Next update date')
    # 结案时间
    enfo_settled_date = fields.Date('Settled date')
    # 其他信息
    enfo_other_info = fields.Text('Other info')


    # 列表信息
    # 立案时间
    list_regist_date = fields.Date('Registration date', compute='_compute_regist_date', store=True)

    @api.depends('arbi_regist_date', 'firs_regist_date', 'seco_regist_date')
    def _compute_regist_date(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_regist_date = record.arbi_regist_date
            elif record.state == 'first_instance':
                record.list_regist_date = record.firs_regist_date
            elif record.state == 'second_instance':
                record.list_regist_date = record.seco_regist_date
            else:
                record.list_regist_date = False

    # 申请人/原告/上诉人/申请执行人
    list_claimant = fields.Char('Claimant/Appellant', compute='_compute_claimant', store=True)

    @api.depends('arbi_claimant', 'firs_claimant','seco_claimant','enfo_claimant')
    def _compute_claimant(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_claimant = record.arbi_claimant
            elif record.state == 'first_instance':
                record.list_claimant = record.firs_claimant
            elif record.state == 'second_instance':
                record.list_claimant = record.seco_claimant
            elif record.state == 'enforcement':
                record.list_claimant = record.enfo_claimant
            else:
                record.list_claimant = False

    # 被申请人/被告/被上诉人/被执行人
    list_respondent = fields.Char('Respondent/Appellee', compute='_compute_respondent', store=True)

    @api.depends('arbi_respondent', 'firs_respondent','seco_respondent','enfo_respondent')
    def _compute_respondent(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_respondent = record.arbi_respondent
            elif record.state == 'first_instance':
                record.list_respondent = record.firs_respondent
            elif record.state == 'second_instance':
                record.list_respondent = record.seco_respondent
            elif record.state == 'enforcement':
                record.list_respondent = record.enfo_respondent
            else:
                record.list_respondent = False

    # 诉讼请求
    list_claim = fields.Char('Claim', compute='_compute_claim', store=True)

    @api.depends('arbi_claim', 'firs_claim','seco_claim','enfo_claim')
    def _compute_claim(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_claim = record.arbi_claim
            elif record.state == 'first_instance':
                record.list_claim = record.firs_claim
            elif record.state == 'second_instance':
                record.list_claim = record.seco_claim
            elif record.state == 'enforcement':
                record.list_claim = record.enfo_claim
            else:
                record.list_claim = False

    # 下次跟踪时间
    list_next_update_date = fields.Char('Next update date', compute='_compute_next_update_date', store=True)

    @api.depends('arbi_next_update_date', 'firs_next_update_date','seco_next_update_date','enfo_next_update_date')
    def _compute_next_update_date(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_next_update_date = record.arbi_next_update_date
            elif record.state == 'first_instance':
                record.list_next_update_date = record.firs_next_update_date
            elif record.state == 'second_instance':
                record.list_next_update_date = record.seco_next_update_date
            elif record.state == 'enforcement':
                record.list_next_update_date = record.enfo_next_update_date
            else:
                record.list_next_update_date = False

    # 是否结案
    list_is_settled = fields.Char('Is settled', compute='_compute_is_settled', store=True)

    @api.depends('arbi_is_settled', 'firs_is_settled','seco_is_settled','enfo_is_settled')
    def _compute_is_settled(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_is_settled = record.arbi_is_settled
            elif record.state == 'first_instance':
                record.list_is_settled = record.firs_is_settled
            elif record.state == 'second_instance':
                record.list_is_settled = record.seco_is_settled
            elif record.state == 'enforcement':
                record.list_is_settled = record.enfo_is_settled
            else:
                record.list_is_settled = False

    # 结案时间
    list_settled_date = fields.Char('Settled date', compute='_compute_settled_date', store=True)

    @api.depends('arbi_settled_date', 'firs_settled_date','seco_settled_date','enfo_settled_date')
    def _compute_settled_date(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_settled_date = record.arbi_settled_date
            elif record.state == 'first_instance':
                record.list_settled_date = record.firs_settled_date
            elif record.state == 'second_instance':
                record.list_settled_date = record.seco_settled_date
            elif record.state == 'enforcement':
                record.list_settled_date = record.enfo_settled_date
            else:
                record.list_settled_date = False

    # 经办人
    list_operator = fields.Char('Operator', compute='_compute_operator', store=True)

    @api.depends('arbi_operator', 'firs_operator','seco_operator','enfo_operator')
    def _compute_operator(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_operator = record.arbi_operator
            elif record.state == 'first_instance':
                record.list_operator = record.firs_operator
            elif record.state == 'second_instance':
                record.list_operator = record.seco_operator
            elif record.state == 'enforcement':
                record.list_operator = record.enfo_operator
            else:
                record.list_operator = False

    # 其他
    list_other_info = fields.Char('Other info', compute='_compute_other_info', store=True)

    @api.depends('arbi_other_info', 'firs_other_info','seco_other_info','enfo_other_info')
    def _compute_other_info(self):
        for record in self:
            if record.state == 'arbitration':
                record.list_other_info = record.arbi_other_info
            elif record.state == 'first_instance':
                record.list_other_info = record.firs_other_info
            elif record.state == 'second_instance':
                record.list_other_info = record.seco_other_info
            elif record.state == 'enforcement':
                record.list_other_info = record.enfo_other_info
            else:
                record.list_other_info = False

    # 通知相关
    last_notify_date = fields.Date(default=fields.Date.today())

    @api.model
    def process_update_notify(self):
        print('lawsuit notify')
        filters = ['&',
                # ('state','=','confirmed')
                ('list_next_update_date', '<=', fields.Datetime.context_timestamp(self,datetime.datetime.now())),
                ('last_notify_date', '<', fields.Date.today()),
                ('list_is_settled', '=', False),
                ]
        results = self.sudo().search(filters)
        print(results)
        # # print(fields.Datetime.context_timestamp(self,datetime.datetime.now()))
        for result in results:
            mail = self.env['mail.thread'].with_context({'safe':True}).message_post(
                    body = _("Your responsible lawsuit need to be updated:<br/>Name: %s<br/>State: %s<br/>Update Date: %s") % (result.name, result.state, result.list_next_update_date),
                    subject = _('Lawsuit update notification.'),
                    partner_ids = [result.response_user_id.partner_id.id,],
                    )
            mail.notification_ids.sudo().write({'is_read':False})
            print(mail)
            # Send wechat message
            wechat_message = _("Your responsible lawsuit need to be updated:<br/>Name: %s<br/>State: %s<br/>Update Date: %s") % (result.name, result.state, result.list_next_update_date)
            if isinstance(wechat_message, tuple):
                wechat_message = wechat_message[0]
            self.send_wechat_message(result.response_user_id, wechat_message)
            # # Redirect 
            result.last_notify_date = fields.Date.today()

    def send_wechat_message(self, user, message):
        wechat = self.env['sce_wechat.wechat'].sudo().search([('is_master','=',True)])
        # logins = user.login.split('@')
        # if wechat and logins[-1]=='sce-re.com':
            # wechat.send_message(logins[0], message)
        wechat.send_message('JinZan', message)

