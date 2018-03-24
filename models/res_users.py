# -*- coding: utf-8 -*-

from openerp.osv import fields, orm

class res_users(orm.Model):
    '''
    Model to add the possibility that the users of the company can configure their IP telephony data
    '''
    _inherit = "res.users"
    _columns = {
        'internal_number': fields.char('Internal Number', size=15,
                                       help="User's internal phone number."),
        'caller_id': fields.char(
            'Caller ID', size=50,
            help="Caller ID used for the calls initiated by this user."),
        'asterisk_chan_type': fields.selection([
            ('SIP', 'SIP'),
            ('PJSIP', 'PJSIP'),
            ('IAX2', 'IAX2'),
            ('DAHDI', 'DAHDI'),
            ('Zap', 'Zap'),
            ('Skinny', 'Skinny'),
            ('MGCP', 'MGCP'),
            ('mISDN', 'mISDN'),
            ('H323', 'H323'),
            ('SCCP', 'SCCP'),
            ('Local', 'Local'),
        ], 'Asterisk Channel Type',
            help="Asterisk channel type, as used in the Asterisk dialplan. "
                 "If the user has a regular IP phone, the channel type is 'SIP'."),
        'resource': fields.char(
            'Resource Name', size=64,
            help="Resource name for the channel type selected. For example, "
                 "if you use 'Dial(SIP/phone1)' in your Asterisk dialplan to ring "
                 "the SIP phone of this user, then the resource name for this user "
                 "is 'phone1'.  For a SIP phone, the phone number is often used as "
                 "resource name, but not always."),
        'asterisk_server_id': fields.many2one(
            'asterisk.server', 'Asterisk Server',
            help="Asterisk server on which the user's phone is connected. "
                 "If you leave this field empty, it will use the first Asterisk "
                 "server of the user's company.")
    }
    _defaults = {
        'asterisk_chan_type': 'SIP',
    }

    def _check_validity(self, cr, uid, ids):
        for user in self.browse(cr, uid, ids):
            strings_to_check = [
                (_('Resource Name'), user.resource),
                (_('Internal Number'), user.internal_number),
                (_('Caller ID'), user.caller_id),
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
                            % (check_string[0], user.name))
        return True

    _constraints = [(
        _check_validity,
        "Error message in raise",
        ['resource', 'internal_number', 'caller_id']
    )]