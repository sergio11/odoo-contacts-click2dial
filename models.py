# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp.tools.translate import _
from openerp import tools, api, addons
from Asterisk import Manager
import logging

_logger = logging.getLogger(__name__)


class asterisk_success_connection_popup(orm.TransientModel):
    _name = 'asterisk.success.connection.popup'
    _description = 'Asterisk Success Connection Popup'
    _columns = {
        'message': fields.char(string="The connection was established successfully, the configured server is operational", readonly=True, store=True)
    }

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

        ast_server = self.browse(cr, uid, ids[0], context=context)
        ast_manager = False

        try:
            ast_manager = Manager.Manager(
                (ast_server.ip_address, ast_server.port),
                ast_server.login,
                ast_server.password)
        except Exception as e:
            raise orm.except_orm(
                _("Connection Test Failed!"),
                _("Here is the error message: %s" % e))
        finally:
            if ast_manager:
                ast_manager.Logoff()
        # Show Modal
        return {
            'name': 'Successful connection to Asterisk',
            'type': 'ir.actions.act_window',
            'res_model': 'asterisk.success.connection.popup',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }


class res_contacts(orm.Model):
    '''Model to refresh and manage contacts'''
    _name = "res.contacts"
    _description = "Contacts"


    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)


    def _get_default_image(self, cr, uid, context=None):
        '''
        Get default user image
        :param cr:
        :param uid:
        :param context:
        :return:
        '''
        image_path = addons.get_module_resource('odoo-contacts-click2dial', 'static/src/img', 'user_default.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    _columns = {
        'first_name': fields.char('First Name', size=50, required=True),
        'surname': fields.char('Surname', size=50, required=True),
        'internal_number': fields.char(
            'Internal Number', size=15,
            help="User's internal phone number."),
        'description': fields.html('Contact Description'),
        'image': fields.binary("Image",
            help="This field holds the image used as image for contact, limited to 1024x1024px.")
    }


    def _check_validity(self, cr, uid, ids):
        for user in self.browse(cr, uid, ids):
            strings_to_check = [
                (_('Internal Number'), user.internal_number),
            ]
            for check_string in strings_to_check:
                if check_string[1]:
                    try:
                        check_string[1].encode('ascii')
                    except UnicodeEncodeError:
                        raise orm.except_orm(
                            _('Error:'),
                            _("The '%s' for the user '%s' should only have "
                              "ASCII caracters")
                            % (check_string[0], user.first_name))
        return True


    _constraints = [(
        _check_validity,
        "Error message in raise",
        ['first_name', 'surname', 'internal_number']
    )]

    defaults = {
        'image': _get_default_image
    }