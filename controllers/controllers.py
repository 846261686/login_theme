# -*- coding: utf-8 -*-
import base64
import functools
import io
import json
import re

import odoo
from addons.web.controllers.main import Home, ensure_db, DataSet, clean_action
from odoo import http
from odoo.http import request
from odoo.modules import get_resource_path
from odoo.tools.mimetypes import guess_mimetype

db_monodb = http.db_monodb


def _login_redirect(self, uid, redirect=None):
    base_url = '/web'
    if request.httprequest.referrer is not None:
        url_params = re.match(r'^.*?(\?.*)\#*', request.httprequest.referrer)
        if url_params is not None:
            base_url += url_params.group(1)
    return redirect if redirect else base_url


Home._login_redirect = _login_redirect


# 重写登录页面接口
class UserLogin(Home):

    @http.route('/web/login', type='http', auth="public", csrf=False)
    def web_login(self, redirect=None, **kw):
        try:
            login_theme = request.env['login.theme.config'].sudo().search([], limit=1)
            request.params['title'] = login_theme.name or 'You Company'
            request.params['english_title'] = login_theme.english_title or 'You Company'
            request.params['copyright_title'] = login_theme.copyright_title or 'You Company'
            request.params['copyright_url'] = login_theme.copyright_url or 'http://www.youcompany.com'
            request.params['footer_display'] = login_theme.footer_display or 'database'

        except BaseException:
            request.params['title'] = 'You Company'
            request.params['english_title'] = 'You Company'
            request.params['copyright_title'] = 'You Company'
            request.params['copyright_url'] = 'http://www.youcompany.com'
        return super().web_login(redirect, **kw)


# 登录验证接口
class UserLoginInterface(http.Controller):
    @http.route('/layui_theme/admin_login', type='http', auth="none", methods=['POST'], sitemap=False,
                csrf=False)
    def layui_theme_admin_login(self, **kw):
        ensure_db()
        res = {
            "isLogin": False,
            "msg": "login fail!",
        }
        login_uid = request.params['login']
        login_pwd = request.params['password']

        uid = request.session.authenticate(request.session.db, login_uid, login_pwd)
        if uid:
            res = {
                "isLogin": True,
                "msg": "login success!",
                "url": "/web?debug=assets"
            }
        return json.dumps(res)


class Binary(http.Controller):
    @http.route([
        '/login_theme/login_background'
    ], type='http', auth="none", cors="*")
    def company_logo(self, dbname=None, **kw):
        imgname = 'login_background'
        imgext = '.jpg'
        placeholder = functools.partial(get_resource_path, 'login_theme', 'static', 'img')
        if request.session.db:
            dbname = request.session.db
        elif dbname is None:
            dbname = db_monodb()
        if not dbname:
            response = http.send_file(placeholder(imgname + imgext))
        else:
            try:
                registry = odoo.modules.registry.Registry(dbname)
                with registry.cursor() as cr:
                    cr.execute("""SELECT login_page_background_image
                                       FROM login_theme_config ORDER BY write_date DESC LIMIT 1
                                  """)
                    row = cr.fetchone()
                    if row and row[0]:
                        image_base64 = base64.b64decode(row[0])
                        image_data = io.BytesIO(image_base64)
                        mimetype = guess_mimetype(image_base64, default='image/png')
                        imgext = '.' + mimetype.split('/')[1]
                        if imgext == '.svg+xml':
                            imgext = '.svg'
                        response = http.send_file(image_data, filename=imgname + imgext, mimetype=mimetype)
                    else:
                        response = http.send_file(placeholder(imgname + imgext))
            except Exception:
                response = http.send_file(placeholder(imgname + imgext))
        return response


class DataSetExtend(DataSet):

    @http.route('/web/dataset/call_button', type='json', auth="user")
    def call_button(self, model, method, args, domain_id=None, context_id=None):
        action = self._call_kw(model, method, args, {})
        if isinstance(action, list) and len(action) > 0:
            actions = []
            for act in action:
                if isinstance(act, dict) and act.get('type') != '':
                    actions.append(clean_action(act))
            if actions:
                return actions
            else:
                return False
        if isinstance(action, dict) and action.get('type') != '':
            return clean_action(action)
        return False
