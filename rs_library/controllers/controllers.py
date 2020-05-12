# -*- coding: utf-8 -*-
from odoo import http

# class RsLibrary(http.Controller):
#     @http.route('/rs_library/rs_library/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rs_library/rs_library/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rs_library.listing', {
#             'root': '/rs_library/rs_library',
#             'objects': http.request.env['rs_library.rs_library'].search([]),
#         })

#     @http.route('/rs_library/rs_library/objects/<model("rs_library.rs_library"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rs_library.object', {
#             'object': obj
#         })