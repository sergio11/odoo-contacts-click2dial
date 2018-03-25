# -*- coding: utf-8 -*-
{
    'name': "odoo-contacts-click2dial",

    'summary': """
        Module for Odoo 8 (OpenERP) to manage contacts and establish VoIP calls through 
        the AMI interface of Asterisk""",

    'description': """
        Module for Odoo 8 (OpenERP) to manage contacts and establish VoIP calls through 
        the AMI interface of Asterisk
    """,

    'author': "Sergio Sánchez Sánchez",
    'website': "https://github.com/sergio11",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'voip',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'templates.xml',
        'views/asterisk_server_view.xml',
        'views/res_contacts_view.xml',
        'views/popup_view.xml',
        'views/res_users_view.xml',
        'views/res_call_history_view.xml'
        #'templates/assets.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}