# from odoo import http


# class LibraryFin(http.Controller):
#     @http.route('/library_fin/library_fin', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/library_fin/library_fin/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('library_fin.listing', {
#             'root': '/library_fin/library_fin',
#             'objects': http.request.env['library_fin.library_fin'].search([]),
#         })

#     @http.route('/library_fin/library_fin/objects/<model("library_fin.library_fin"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('library_fin.object', {
#             'object': obj
#         })

