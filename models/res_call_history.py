# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp import tools, addons, api
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class res_call_history(orm.Model):
    '''Model to store the call history'''
    _name = 'res.call.history'
    _description = 'Call History'
    _columns = {
        'user': fields.many2one('res.users', 'User',
                                help='User who made the call', required=True, ondelete='cascade'),
        'contact': fields.many2one('res.contacts', 'Contact',
                                   help='Contact that has been called', required=True, ondelete='cascade'),
        'start_date': fields.date('Start Date', required=True)
    }
    _defaults = {
        'start_date': fields.date.context_today
    }

