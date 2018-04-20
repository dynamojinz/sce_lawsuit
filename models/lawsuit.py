# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import _
import datetime


# CHECKED_FIELDS = [ 'floor_area', 'plot_ratio', 'volume_area', 'residential_area', 'bussiness_area',
                    # 'office_area', 'other_area', 'site_situation', 'transfer_price',
                    # 'voice_cost', 'floor_price', 'estimate_sale_price', 'saler_introduction',
                    # 'saler_core_requirement', 'agent_introduction', 'debt_situation',
                    # 'product_value', 'net_profit_rate', 'base_judgement']
class LawsuitType(models.Model):
    _name = 'sce_lawsuit.type'
    name = fields.Char()

class Lawsuit(models.Model):
    _name = 'sce_lawsuit.lawsuit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # 案件名称
    name = fields.Char(required=True)
    # 项目名称(涉诉项目）:
    project_name = fields.Char()
    # 案件类型
    type_id  = fields.Many2one('sce_lawsuit.type', string='Lawsuit Type')
    # 区域
    region = fields.Char(required=True)
    # 案由
    cause = fields.Text(required=True)
    # 阶段
    state = fields.Selection(selection=[
            ('arbitration','Arbitration'),             # 仲裁
            ('first_instance','First Instance'),       # 一审
            ('second_instance','Second Instance'),     # 二审
            ('enforcement','Enforcement'),             # 执行
            ('retrial', 'Retrial'),                    # 再审
        ],default='first_instance')
    # 是否有仲裁
    has_arbi = fields.Boolean('Has arbitration state?')
    # 是否有再审
    has_retr = fields.Boolean('Has retrial state?')
    # 下次跟踪时间
    next_update_date = fields.Date('Next update date', required=True)
    # 经办人
    response_user_id = fields.Many2one('res.users', default=lambda self:self.env.user, readonly=True)

    ### 仲裁阶段 ###
    ## 立案信息
    # 立案时间
    arbi_regist_date = fields.Date('Registration date', states={'arbitration':[('required',True)]})
    # 案号
    arbi_no = fields.Char('Case Number')
    # 经办人
    arbi_operator = fields.Char('Operator', states={'arbitration':[('required',True)]})
    # 申请人
    arbi_claimant = fields.Char('Arbitration claimant', states={'arbitration':[('required',True)]})
    # 被申请人
    arbi_respondent = fields.Char('Arbitration respondent', states={'arbitration':[('required',True)]})
    # 第三人
    arbi_third_party = fields.Char('Third party')
    # 标的(金额)
    arbi_subject = fields.Char('Subject(amount of money)')
    # 仲裁请求
    arbi_claim = fields.Text('Arbitration claim', states={'arbitration':[('required',True)]})
    # 仲裁机构
    arbi_court = fields.Char('Arbitration organization')
    # 仲裁员
    arbi_judge = fields.Char('Arbitrator')
    # 仲裁员联系方式
    arbi_judge_tel= fields.Char('Arbitrator telephone')
    # 诉讼保全
    arbi_has_preservation = fields.Boolean('Has preservation?')
    arbi_preservation = fields.Char('Arbitration preservation')
    # 外聘律所及律师 
    arbi_has_external = fields.Boolean('Has external?')
    arbi_external_lawyer = fields.Char('External lawyer')

    ## 庭审信息
    # 首次开庭时间
    arbi_open_date = fields.Date('Frist opening date', resquired=True)
    # 历次开庭记录
    arbi_trial_records = fields.Text('Court trial records')
    # 庭审资料

    ## 结案信息
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

    ## 附件
    # 立案资料
    arbi_docs_claimant = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','arbi_docs_respondent')],
            string='Arbitration claimant documents')
    arbi_docs_claimant_count = fields.Integer('Claimant docs count', compute='_compute_arbi_docs_claimant_count')
    arbi_docs_respondent = fields.One2many('ir.attachment','res_id', 
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','arbi_docs_respondent')],
            string='Arbitration respondent documents')
    arbi_docs_respondent_count = fields.Integer('Respondent docs count', compute='_compute_arbi_docs_respondent_count')

    @api.multi
    def action_get_attachment_tree_view_arbi_docs_claimant(self):
        return self._action_get_attachment_tree_view('arbi_docs_claimant')

    @api.multi
    def action_get_attachment_tree_view_arbi_docs_respondent(self):
        return self._action_get_attachment_tree_view('arbi_docs_respondent')

    @api.depends('arbi_docs_claimant')
    def _compute_arbi_docs_claimant_count(self):
        self._compute_attachment_count('arbi_docs_claimant')

    @api.depends('arbi_docs_respondent')
    def _compute_arbi_docs_respondent_count(self):
        self._compute_attachment_count('arbi_docs_respondent')

    # 庭审资料
    arbi_docs_trial = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','arbi_docs_trial')],
            string='Arbitration trial documents')
    arbi_docs_trial_count = fields.Integer('Trial docs count', compute='_compute_arbi_docs_trial_count')

    @api.multi
    def action_get_attachment_tree_view_arbi_docs_trial(self):
        return self._action_get_attachment_tree_view('arbi_docs_trial')

    @api.depends('arbi_docs_trial')
    def _compute_arbi_docs_trial_count(self):
        self._compute_attachment_count('arbi_docs_trial')

    # 审结资料
    arbi_docs_settle = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','arbi_docs_settle')],
            string='Arbitration settle documents')
    arbi_docs_settle_count = fields.Integer('Settle docs count', compute='_compute_arbi_docs_settle_count')

    @api.multi
    def action_get_attachment_tree_view_arbi_docs_settle(self):
        return self._action_get_attachment_tree_view('arbi_docs_settle')

    @api.depends('arbi_docs_settle')
    def _compute_arbi_docs_settle_count(self):
        self._compute_attachment_count('arbi_docs_settle')




    ### 一审阶段 ###
    ## 立案信息
    # 立案时间
    firs_regist_date = fields.Date('Registration date', states={'first_instance':[('required',True)]})
    # 案号
    firs_no = fields.Char('Case Number')
    # 经办人
    firs_operator = fields.Char('Operator', states={'first_instance':[('required',True)]})
    # 原告
    firs_claimant = fields.Char('Claimant', states={'first_instance':[('required',True)]})
    # 被告
    firs_respondent = fields.Char('Respondent', states={'first_instance':[('required',True)]})
    # 第三人
    firs_third_party = fields.Char('Third party')
    # 标的(金额)
    firs_subject = fields.Char('Subject(amount of money)')
    # 诉讼请求
    firs_claim = fields.Text('Claim', states={'first_instance':[('required',True)]})
    # 审理法院
    firs_court = fields.Char('Trial court')
    # 经办法官
    firs_judge = fields.Char('Frist Judge')
    # 法官联系方式
    firs_judge_tel= fields.Char('Judge telephone')
    # 诉讼保全
    firs_has_preservation = fields.Boolean('Has preservation?')
    firs_preservation = fields.Char('Arbitration preservation')
    # 外聘律所及律师 
    firs_has_external = fields.Boolean('Has external?')
    firs_external_lawyer = fields.Char('External lawyer')
    # 是否反诉
    firs_has_counterclaim = fields.Boolean('Has counterclaim?')
    firs_counterclaim = fields.Char('Counterclaim')

    ## 庭审信息
    # 首次开庭时间
    firs_open_date = fields.Date('Frist opening date', resquired=True)
    # 历次开庭记录
    firs_trial_records = fields.Text('Court trial records')
    # 庭审资料

    ## 结案信息
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

    ## 附件
    # 立案资料
    firs_docs_claimant = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','firs_docs_respondent')],
            string='Claimant documents')
    firs_docs_claimant_count = fields.Integer('Claimant docs count', compute='_compute_firs_docs_claimant_count')
    firs_docs_respondent = fields.One2many('ir.attachment','res_id', 
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','firs_docs_respondent')],
            string='Respondent documents')
    firs_docs_respondent_count = fields.Integer('Respondent docs count', compute='_compute_firs_docs_respondent_count')

    @api.multi
    def action_get_attachment_tree_view_firs_docs_claimant(self):
        return self._action_get_attachment_tree_view('firs_docs_claimant')

    @api.multi
    def action_get_attachment_tree_view_firs_docs_respondent(self):
        return self._action_get_attachment_tree_view('firs_docs_respondent')

    @api.depends('firs_docs_claimant')
    def _compute_firs_docs_claimant_count(self):
        self._compute_attachment_count('firs_docs_claimant')

    @api.depends('firs_docs_respondent')
    def _compute_firs_docs_respondent_count(self):
        self._compute_attachment_count('firs_docs_respondent')

    # 庭审资料
    firs_docs_trial = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','firs_docs_trial')],
            string='Trial documents')
    firs_docs_trial_count = fields.Integer('Trial docs count', compute='_compute_firs_docs_trial_count')

    @api.multi
    def action_get_attachment_tree_view_firs_docs_trial(self):
        return self._action_get_attachment_tree_view('firs_docs_trial')

    @api.depends('firs_docs_trial')
    def _compute_firs_docs_trial_count(self):
        self._compute_attachment_count('firs_docs_trial')

    # 审结资料
    firs_docs_settle = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','firs_docs_settle')],
            string='Settle documents')
    firs_docs_settle_count = fields.Integer('Settle docs count', compute='_compute_firs_docs_settle_count')

    @api.multi
    def action_get_attachment_tree_view_firs_docs_settle(self):
        return self._action_get_attachment_tree_view('firs_docs_settle')

    @api.depends('firs_docs_settle')
    def _compute_firs_docs_settle_count(self):
        self._compute_attachment_count('firs_docs_settle')



    ### 二审阶段 ###
    ## 立案信息
    # 立案时间
    seco_regist_date = fields.Date('Registration date', states={'second_instance':[('required',True)]})
    # 案号
    seco_no = fields.Char('Case Number')
    # 经办人
    seco_operator = fields.Char('Operator', states={'second_instance':[('required',True)]})
    # 上诉人 
    seco_claimant = fields.Char('Appellant', states={'second_instance':[('required',True)]})
    # 被上诉人
    seco_respondent = fields.Char('Appellee', states={'second_instance':[('required',True)]})
    # 第三人
    seco_third_party = fields.Char('Third party')
    # 标的(金额)
    seco_subject = fields.Char('Subject(amount of money)')
    # 上诉请求
    seco_claim = fields.Text('Appeals request', states={'second_instance':[('required',True)]})
    # 审理法院
    seco_court = fields.Char('Trial court')
    # 经办法官
    seco_judge = fields.Char('Second Judge')
    # 法官联系方式
    seco_judge_tel= fields.Char('Judge telephone')
    # 诉讼保全
    seco_has_preservation = fields.Boolean('Has preservation?')
    seco_preservation = fields.Char('Arbitration preservation')
    # 外聘律所及律师 
    seco_has_external = fields.Boolean('Has external?')
    seco_external_lawyer = fields.Char('External lawyer')

    ## 庭审信息
    # 首次开庭时间
    seco_open_date = fields.Date('Frist opening date', resquired=True)
    # 历次开庭记录
    seco_trial_records = fields.Text('Court trial records')
    # 庭审资料

    ## 结案信息
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

    ## 附件
    # 立案资料
    seco_docs_claimant = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','seco_docs_respondent')],
            string='Claimant documents')
    seco_docs_claimant_count = fields.Integer('Claimant docs count', compute='_compute_seco_docs_claimant_count')
    seco_docs_respondent = fields.One2many('ir.attachment','res_id', 
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','seco_docs_respondent')],
            string='Respondent documents')
    seco_docs_respondent_count = fields.Integer('Respondent docs count', compute='_compute_seco_docs_respondent_count')

    @api.multi
    def action_get_attachment_tree_view_seco_docs_claimant(self):
        return self._action_get_attachment_tree_view('seco_docs_claimant')

    @api.multi
    def action_get_attachment_tree_view_seco_docs_respondent(self):
        return self._action_get_attachment_tree_view('seco_docs_respondent')

    @api.depends('seco_docs_claimant')
    def _compute_seco_docs_claimant_count(self):
        self._compute_attachment_count('seco_docs_claimant')

    @api.depends('seco_docs_respondent')
    def _compute_seco_docs_respondent_count(self):
        self._compute_attachment_count('seco_docs_respondent')

    # 庭审资料
    seco_docs_trial = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','seco_docs_trial')],
            string='Trial documents')
    seco_docs_trial_count = fields.Integer('Trial docs count', compute='_compute_seco_docs_trial_count')

    @api.multi
    def action_get_attachment_tree_view_seco_docs_trial(self):
        return self._action_get_attachment_tree_view('seco_docs_trial')

    @api.depends('seco_docs_trial')
    def _compute_seco_docs_trial_count(self):
        self._compute_attachment_count('seco_docs_trial')

    # 审结资料
    seco_docs_settle = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','seco_docs_settle')],
            string='Settle documents')
    seco_docs_settle_count = fields.Integer('Settle docs count', compute='_compute_seco_docs_settle_count')

    @api.multi
    def action_get_attachment_tree_view_seco_docs_settle(self):
        return self._action_get_attachment_tree_view('seco_docs_settle')

    @api.depends('seco_docs_settle')
    def _compute_seco_docs_settle_count(self):
        self._compute_attachment_count('seco_docs_settle')



    ### 执行阶段 ###
    ## 立案信息
    # 立案时间
    enfo_regist_date = fields.Date('Registration date', states={'enforcement':[('required',True)]})
    # 案号
    enfo_no = fields.Char('Case Number')
    # 经办人
    enfo_operator = fields.Char('Operator', states={'enforcement':[('required',True)]})
    # 申请执行人 
    enfo_claimant = fields.Char('Claimant', states={'enforcement':[('required',True)]})
    # 被执行人 
    enfo_respondent = fields.Char('Respondent', states={'enforcement':[('required',True)]})
    # 第三人, 执行阶段无此信息
    # enfo_third_party = fields.Char('Third party')
    # 执行标的(金额)
    enfo_subject = fields.Char('Enforcement subject(amount of money)')
    # 执行请求
    enfo_claim = fields.Text('Claim', states={'enforcement':[('required',True)]})
    # 执行进展/结果
    enfo_result = fields.Text('Enforcement progress/results', states={'enforcement':[('required',True)]})
    # 执行法院
    enfo_court = fields.Char('Enforcement court')
    # 经办法官
    enfo_judge = fields.Char('Enforcement Judge')
    # 法官联系方式
    enfo_judge_tel= fields.Char('Judge telephone')
    # 被执行人财产线索
    enfo_has_clue = fields.Boolean('Has respondent property clue?')
    enfo_property_clue = fields.Char('Respondent property clue')
    # 外聘律所及律师 
    enfo_has_external = fields.Boolean('Has external?')
    enfo_external_lawyer = fields.Char('External lawyer')

    ## 庭审信息
    # # 首次开庭时间
    # enfo_open_date = fields.Date('Frist opening date', resquired=True)
    # 申请执行时间
    # enfo_apply_date = fields.Date('Application enforcement date')

    ## 结案信息
    # 是否结案
    enfo_is_settled = fields.Boolean('Is settled', states={'enforcement':[('required',True)]})
    # # 是否需申请执行
    # enfo_need_enforcement = fields.Boolean('Need enforcement?')
    # 下次跟踪时间
    enfo_next_update_date = fields.Date('Next update date')
    # 结案时间
    enfo_settled_date = fields.Date('Settled date')
    # 其他信息
    enfo_other_info = fields.Text('Other info')

    ## 附件
    # 立案资料
    enfo_docs_claimant = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','enfo_docs_respondent')],
            string='Enforcement Claimant documents')
    enfo_docs_claimant_count = fields.Integer('Claimant docs count', compute='_compute_enfo_docs_claimant_count')

    @api.multi
    def action_get_attachment_tree_view_enfo_docs_claimant(self):
        return self._action_get_attachment_tree_view('enfo_docs_claimant')

    @api.depends('enfo_docs_claimant')
    def _compute_enfo_docs_claimant_count(self):
        self._compute_attachment_count('enfo_docs_claimant')

    # 审结资料
    enfo_docs_settle = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','enfo_docs_settle')],
            string='Settle documents')
    enfo_docs_settle_count = fields.Integer('Settle docs count', compute='_compute_enfo_docs_settle_count')

    @api.multi
    def action_get_attachment_tree_view_enfo_docs_settle(self):
        return self._action_get_attachment_tree_view('enfo_docs_settle')

    @api.depends('enfo_docs_settle')
    def _compute_enfo_docs_settle_count(self):
        self._compute_attachment_count('enfo_docs_settle')




    ### 再审阶段 ###
    ## 立案信息
    # 立案时间
    retr_regist_date = fields.Date('Registration date', states={'retrial':[('required',True)]})
    # 案号
    retr_no = fields.Char('Case Number')
    # 经办人
    retr_operator = fields.Char('Operator', states={'retrial':[('required',True)]})
    # 再审申请人 
    retr_claimant = fields.Char('Claimant', states={'retrial':[('required',True)]})
    # 被审请人 
    retr_respondent = fields.Char('Respondent', states={'retrial':[('required',True)]})
    # 第三人
    retr_third_party = fields.Char('Third party')
    # 标的(金额)
    retr_subject = fields.Char('Subject(amount of money)')
    # 再审请求
    retr_claim = fields.Text('Claim', states={'retrial':[('required',True)]})
    # 诉讼进展/结果
    retr_result = fields.Text('Retrial progress/results', states={'retrial':[('required',True)]})
    # 审理法院
    retr_court = fields.Char('Trial court')
    # 经办法官
    retr_judge = fields.Char('Retrial Judge')
    # 法官联系方式
    retr_judge_tel= fields.Char('Judge telephone')
    # 诉讼保全
    retr_has_preservation = fields.Boolean('Has preservation?')
    retr_preservation = fields.Char('Arbitration preservation')
    # 外聘律所及律师 
    retr_has_external = fields.Boolean('Has external?')
    retr_external_lawyer = fields.Char('External lawyer')
    # # 首次开庭时间
    # retr_open_date = fields.Date('Frist opening date', resquired=True)
    # 申请执行时间
    # retr_apply_date = fields.Date('Application retrrcement date')
    # # 是否需申请执行
    # retr_need_retrrcement = fields.Boolean('Need retrrcement?')

    ## 结案信息
    # 是否结案
    retr_is_settled = fields.Boolean('Is settled', states={'retrial':[('required',True)]})
    # 下次跟踪时间
    retr_next_update_date = fields.Date('Next update date')
    # 结案时间
    retr_settled_date = fields.Date('Settled date')
    # 其他信息
    retr_other_info = fields.Text('Other info')

    ## 附件
    # 立案资料
    retr_docs_claimant = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','retr_docs_respondent')],
            string='Retrial claimant documents')
    retr_docs_claimant_count = fields.Integer('Claimant docs count', compute='_compute_retr_docs_claimant_count')
    retr_docs_respondent = fields.One2many('ir.attachment','res_id', 
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','retr_docs_respondent')],
            string='Retrial respondent documents')
    retr_docs_respondent_count = fields.Integer('Respondent docs count', compute='_compute_retr_docs_respondent_count')

    @api.multi
    def action_get_attachment_tree_view_retr_docs_claimant(self):
        return self._action_get_attachment_tree_view('retr_docs_claimant')

    @api.multi
    def action_get_attachment_tree_view_retr_docs_respondent(self):
        return self._action_get_attachment_tree_view('retr_docs_respondent')

    @api.depends('retr_docs_claimant')
    def _compute_retr_docs_claimant_count(self):
        self._compute_attachment_count('retr_docs_claimant')

    @api.depends('retr_docs_respondent')
    def _compute_retr_docs_respondent_count(self):
        self._compute_attachment_count('retr_docs_respondent')

    # 审结资料
    retr_docs_settle = fields.One2many('ir.attachment','res_id',
            domain=['&',('res_model','=','sce_lawsuit.lawsuit'),('res_field','=','retr_docs_settle')],
            string='Settle documents')
    retr_docs_settle_count = fields.Integer('Settle docs count', compute='_compute_retr_docs_settle_count')

    @api.multi
    def action_get_attachment_tree_view_retr_docs_settle(self):
        return self._action_get_attachment_tree_view('retr_docs_settle')

    @api.depends('retr_docs_settle')
    def _compute_retr_docs_settle_count(self):
        self._compute_attachment_count('retr_docs_settle')


    ###  列表信息 ###
    # 申请人/原告/上诉人/申请执行人
    list_claimant = fields.Char('Claimant/Appellant', compute='_compute_claimant', store=True, help="Original claimant(arbitration claimant or first instance claimant).")

    @api.depends('arbi_claimant', 'firs_claimant')
    def _compute_claimant(self):
        for record in self:
            if record.has_arbi:
                record.list_claimant = record.arbi_claimant
            else:
                record.list_claimant = record.firs_claimant

    # 被申请人/被告/被上诉人/被执行人
    list_respondent = fields.Char('Respondent/Appellee', compute='_compute_respondent', store=True, help="Original respondent(arbitration respondent or first instance respondent)")

    @api.depends('arbi_respondent', 'firs_respondent')
    def _compute_respondent(self):
        for record in self:
            if record.has_arbi:
                record.list_respondent = record.arbi_respondent
            else:
                record.list_respondent = record.firs_respondent

    # 立案时间
    list_regist_date = fields.Char('Regist date', compute='_compute_regist_date', store=True, help="Original regist date(arbitration or first instance)")

    @api.depends('arbi_regist_date', 'firs_regist_date')
    def _compute_regist_date(self):
        for record in self:
            if record.has_arbi:
                record.list_regist_date = record.arbi_regist_date
            else:
                record.list_regist_date = record.firs_regist_date


    # 是否结案
    list_is_settled = fields.Char('Is settled', compute='_compute_is_settled', store=True, help="If now state has settled")

    @api.depends('arbi_is_settled', 'firs_is_settled','seco_is_settled','enfo_is_settled','retr_is_settled')
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
            elif record.state == 'retrial':
                record.list_is_settled = record.retr_is_settled
            else:
                record.list_is_settled = False


    # 附件相关
    @api.multi
    def _action_get_attachment_tree_view(self, res_field):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model':self._name,'default_res_id':self.ids[0], 'default_res_field':res_field}
        action['domain'] = str(['&', ('res_model', '=', self._name),('res_field','=',res_field),('res_id', 'in', self.ids)])
        return action

    @api.multi
    def _compute_attachment_count(self, res_field):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model','=',self._name),('res_field','=',res_field),('res_id','in',self.ids)],
            ['res_id'],['res_id']
            )
        attachdata = dict((res['res_id'],res['res_id_count']) for res in read_group_res)
        for record in self:
            record[res_field+"_count"] = attachdata.get(record.id,0)

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

