# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import config


class LoginThemeConfig(models.Model):
    _name = 'login.theme.config'
    _description = '主题设置'

    name = fields.Char('登录页标题', default=config.get('login_zh_title', 'YouCompany'))
    english_title = fields.Char('登录页英文标题', default=config.get('login_en_title', 'YouCompany'))
    web_title = fields.Char('网页标题', default='YouCompany')
    dialog_title = fields.Char('弹出框标题', default='YouCompany')
    copyright_title = fields.Char('版权信息', default='YouCompany')
    copyright_url = fields.Char('版权地址', default='http://www.funenc.com')
    login_page_background_image = fields.Binary(string='登录页面背景图')
    background_color = fields.Char(string='背景色')
    footer_display = fields.Selection([('database', '数据库管理'), ('company', '公司信息')], string='页脚显示')

    @api.model
    def jump_form_edit(self):
        """
        直接跳转 form视图
        :return:
        """
        action = self.env.ref('login_theme.login_theme_config_act_window').read()[0]
        record = self.search([], limit=1)
        if record:
            action['res_id'] = record.id
        action['context'] = {'form_view_initial_mode': 'edit'}
        action['target'] = "new"
        return action


