# -*- coding: utf-8 -*-

from openerp.osv import fields, orm

class asterisk_success_connection_popup(orm.TransientModel):
    _name = 'asterisk.success.connection.popup'
    _description = 'Asterisk Success Connection Popup'
    _columns = {
        'message': fields.char(string="The connection was established successfully, the configured server is operational", readonly=True, store=True)
    }


class asterisk_call_originated_successfully_popup(orm.TransientModel):
    _name = 'asterisk.call.originated.successfully.popup'
    _description = 'Asterisk Call Originated Successfully Popup'
    _columns = {
        'message': fields.char(string="The call was originated successfully, soon you can start the conversation from your configured ip terminal", readonly=True, store=True)
    }