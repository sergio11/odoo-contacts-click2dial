# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp import tools, addons, api, osv
from openerp.tools.translate import _
import re
import logging

_logger = logging.getLogger(__name__)

class res_contacts(orm.Model):
    '''Model to refresh and manage contacts'''
    _name = 'res.contacts'
    _inherit = 'phone.common'
    _description = 'Contacts'
    _rec_name = 'display_name'

    @api.one
    @api.depends('first_name', 'surname')
    def _compute_display_name(self):
        '''
        Method to set the value of the contact's full name
        :return:
        '''
        self.display_name = "%s - %s" % (self.first_name, self.surname)


    def _check_validity(self, cr, uid, ids):
        '''
        Function to check the integrity of text fields
        :param cr:
        :param uid:
        :param ids:
        :return:
        '''
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
            # Validate User Email
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", user.email) == None:
                raise orm.except_orm('Invalid Email', 'Please enter a valid email address')

        return True

    _columns = {
        'first_name': fields.char('First Name', size=50, required=True),
        'surname': fields.char('Surname', size=50, required=True),
        'display_name': fields.char("Display Name", compute="_compute_display_name",
                                 help='Contact Display name', store=True),
        'email': fields.char("Email", required=True),
        'internal_number': fields.char(
            'Internal Number', size=15,
            help="User's internal phone number."),
        'description': fields.html('Contact Description'),
        'image': fields.binary("Contact Image",
            help="This field holds the image used as image for contact, limited to 1024x1024px.", required=True)
    }


    _constraints = [(
        _check_validity,
        "Error message in raise",
        ['first_name', 'surname', 'internal_number']
    )]

    def click2dial(self, cr, uid, ids, context=None):
        '''
        Dial to contact
        :return:
        '''

        res = super(res_contacts, self).click2dial(cr, uid, ids, context=context)

        # Show Modal
        return {
            'name': _('Call to %s originated successfully')
                % res['dialed_number'],
            'type': 'ir.actions.act_window',
            'res_model': 'asterisk.call.originated.successfully.popup',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }