# -*- coding: utf-8 -*-
from openerp import http

# class Odoo-contacts-click2dial(http.Controller):
#     @http.route('/odoo-contacts-click2dial/odoo-contacts-click2dial/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-contacts-click2dial/odoo-contacts-click2dial/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-contacts-click2dial.listing', {
#             'root': '/odoo-contacts-click2dial/odoo-contacts-click2dial',
#             'objects': http.request.env['odoo-contacts-click2dial.odoo-contacts-click2dial'].search([]),
#         })

#     @http.route('/odoo-contacts-click2dial/odoo-contacts-click2dial/objects/<model("odoo-contacts-click2dial.odoo-contacts-click2dial"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-contacts-click2dial.object', {
#             'object': obj
#         })