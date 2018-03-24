# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp import tools, addons
import logging

_logger = logging.getLogger(__name__)

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

    def click2dial(self, cr, uid, ids, context=None):
        '''
        Dial to contact
        :return:
        '''

        # Show Modal
        return {
            'name': 'Call originated successfully',
            'type': 'ir.actions.act_window',
            'res_model': 'asterisk.call.originated.successfully.popup',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }