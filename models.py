# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp.tools.translate import _
import logging

class asterisk_server(orm.Model):
    '''Asterisk server object, stores the parameters of the Asterisk IPBXs'''
    _name = "asterisk.server"
    _description = "Asterisk Servers"
    _columns = {
        'name': fields.char('Asterisk Server Name', size=50, required=True),
        'active': fields.boolean(
            'Active', help="The active field allows you to hide the Asterisk "
                           "server without deleting it."),
        'ip_address': fields.char(
            'Asterisk IP address or DNS', size=50, required=True,
            help="IP address or DNS name of the Asterisk server."),
        'port': fields.integer(
            'Port', required=True,
            help="TCP port on which the Asterisk Manager Interface listens. "
                 "Defined in /etc/asterisk/manager.conf on Asterisk."),
        'login': fields.char(
            'AMI Login', size=30, required=True,
            help="Login that Odoo will use to communicate with the "
                 "Asterisk Manager Interface. Refer to /etc/asterisk/manager.conf "
                 "on your Asterisk server."),
        'password': fields.char(
            'AMI Password', size=30, required=True,
            help="Password that Odoo will use to communicate with the "
                 "Asterisk Manager Interface. Refer to /etc/asterisk/manager.conf "
                 "on your Asterisk server."),
        'context': fields.char(
            'Dialplan Context', size=50, required=True,
            help="Asterisk dialplan context from which the calls will be "
                 "made. Refer to /etc/asterisk/extensions.conf on your Asterisk "
                 "server."),
        'extension_priority': fields.integer(
            'Extension Priority', required=True,
            help="Priority of the extension in the Asterisk dialplan. Refer "
                 "to /etc/asterisk/extensions.conf on your Asterisk server."),
        'wait_time': fields.integer(
            'Wait Time (sec)', required=True,
            help="Amount of time (in seconds) Asterisk will try to reach "
                 "the user's phone before hanging up."),
        'company_id': fields.many2one(
            'res.company', 'Company',
            help="Company who uses the Asterisk server.")
    }

    _defaults = {
        'active': True,
        'port': 5038,  # Default AMI port
        'extension_priority': 1,
        'wait_time': 15,
        'company_id': lambda self, cr, uid, context:
        self.pool['res.company']._company_default_get(
            cr, uid, 'asterisk.server', context=context),
    }



    def _check_validity(self, cr, uid, ids):
        '''
        Check Validity
        :param cr:
        :param uid:
        :param ids:
        :return:
        '''
        for server in self.browse(cr, uid, ids):

            for check_str in [
                ('Dialplan context', server.context),
                ('AMI login', server.login),
                ('AMI password', server.password)]:
                if check_str[1]:
                    try:
                        check_str[1].encode('ascii')
                    except UnicodeEncodeError:
                        raise orm.except_orm(
                            _('Error:'),
                            _("The '%s' should only have ASCII caracters for "
                              "the Asterisk server '%s'"
                              % (check_str[0], server.name)))

            if server.wait_time < 1 or server.wait_time > 120:
                raise orm.except_orm(
                    _('Error:'),
                    _("You should set a 'Wait time' value between 1 and 120 "
                      "seconds for the Asterisk server '%s'" % server.name))
            if server.extension_priority < 1:
                raise orm.except_orm(
                    _('Error:'),
                    _("The 'extension priority' must be a positive value for "
                      "the Asterisk server '%s'" % server.name))
            if server.port > 65535 or server.port < 1:
                raise orm.except_orm(
                    _('Error:'),
                    _("You should set a TCP port between 1 and 65535 for the "
                      "Asterisk server '%s'" % server.name))

            return True

    _constraints = [(
        _check_validity,
        "Error message in raise",
        [
            'out_prefix', 'wait_time', 'extension_priority', 'port',
            'context', 'alert_info', 'login', 'password']
    )]

    def _connect_to_asterisk(self, cr, uid, context=None):
        '''
        Open the connection to the Asterisk Manager
        Returns an instance of the Asterisk Manager
        '''

    def test_ami_connection(self, cr, uid, ids, context=None):
        '''
        Test Ami Connection
        :param cr:
        :param uid:
        :param ids:
        :param context:
        :return:
        '''
