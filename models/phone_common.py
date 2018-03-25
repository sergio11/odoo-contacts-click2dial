# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp.tools.translate import _
from Asterisk import Manager
import logging

_logger = logging.getLogger(__name__)

class phone_common(orm.AbstractModel):
    _name = 'phone.common'

    def click2dial(self, cr, uid, ids, context=None):

        # Search Contact
        contacts = self.pool.get('res.contacts').browse(cr, uid, ids)

        if not len(contacts) or not contacts[0].internal_number:
            raise orm.except_orm(
                _('Error:'),
                _('The call can not be made'))


        # Connect to Asterisk Server
        user, ast_server, ast_manager = \
            self.pool['asterisk.server']._connect_to_asterisk(
                cr, uid, context=context)

        # The user should have a CallerID
        if not user.caller_id:
            raise orm.except_orm(
                _('Error:'),
                _('No callerID configured for the current user'))


        channel = '%s/%s' % (user.asterisk_chan_type, user.resource)

        _logger.info("Call to %s with internal number %s from caller id %s on channel %s on context %s" % (contacts[0].first_name
                                                             , contacts[0].internal_number, user.caller_id, channel, ast_server.context))

        try:
            # Originate Call
            ast_manager.Originate(
                channel,
                context=ast_server.context,
                extension=contacts[0].internal_number,
                priority=str(ast_server.extension_priority),
                timeout=str(ast_server.wait_time * 1000),
                caller_id=user.caller_id)

            # Register Call
            self.pool.get('res.call.history').create(cr, uid, {
                'user': user.id, 'contact': contacts[0].id}, context=context)

        except Exception as e:
            _logger.error(
                "Error in the Originate request to Asterisk server %s"
                % ast_server.ip_address)
            _logger.error(
                "Here are the details of the error: '%s'" % str(e))
            raise orm.except_orm(
                _('Error:'),
                _("Click to dial with Asterisk failed.\nHere is the error: "
                    "'%s'")
                % str(e))
        finally:
            ast_manager.Logoff()

        return {'dialed_number': contacts[0].internal_number}