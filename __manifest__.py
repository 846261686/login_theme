# -*- coding: utf-8 -*-
{
    'name': "login_theme",

    'summary': """
        Rewrite the odoo login interface to make it configurable""",

    'description': """
       Rewrite the odoo login interface to make it configurable
    """,

    'author': "Li",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/login.xml',
        'views/login_theme.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
