# -*- coding: utf-8 -*-
# from odoo import http


# class PayslipAttendence(http.Controller):
#     @http.route('/payslip_attendence/payslip_attendence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payslip_attendence/payslip_attendence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payslip_attendence.listing', {
#             'root': '/payslip_attendence/payslip_attendence',
#             'objects': http.request.env['payslip_attendence.payslip_attendence'].search([]),
#         })

#     @http.route('/payslip_attendence/payslip_attendence/objects/<model("payslip_attendence.payslip_attendence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payslip_attendence.object', {
#             'object': obj
#         })
