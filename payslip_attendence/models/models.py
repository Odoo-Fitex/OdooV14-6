# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    employee_attendance_ids = fields.One2many('hr.attendance', 'payslip_id')
    employee_shift_ids = fields.One2many('employee.shift.line', 'payslip_id')
    employee_overtime_ids = fields.One2many('hr.overtime', 'payslip_id')

    def load_emp_attendance(self):
        if not (self.employee_id and self.date_from and self.date_to):
            raise UserError(_("Please select an employee first or enter dates"))

        attendances = self.env['hr.attendance'].search([('employee_id', '=', self.employee_id.id),
                                                        ('check_in', '>=', self.date_from),
                                                        ('check_in', '<=', self.date_to),
                                                        ])
        print("attendances", attendances)
        if attendances:
            for att in attendances:
                att.write({'payslip_id': self.id})

    @api.onchange('employee_id')
    def load_emp_shifts(self):
        self.employee_shift_ids = self.get_shift_lines()

    def get_shift_lines(self):
        shifts = self.env['employee.shift.line'].search([('employee_id', '=', self.employee_id.id),
                                                         ('date_from', '>=', self.date_from),
                                                         ('date_from', '<=', self.date_to),
                                                         ])
        return shifts

    @api.onchange('employee_id')
    def load_emp_overtime(self):
        self.employee_overtime_ids = self.get_overtime_lines()

    def get_overtime_lines(self):
        overtimes = self.env['hr.overtime'].search([('employee_id', '=', self.employee_id.id),
                                                    ('date_from', '>=', self.date_from),
                                                    ('date_from', '<=', self.date_to),
                                                    ('state', '=', 'approved')
                                                    ])
        return overtimes


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    payslip_id = fields.Many2one('hr.payslip')


class EmployeeShiftLine(models.Model):
    _inherit = 'employee.shift.line'

    payslip_id = fields.Many2one('hr.payslip')


class HrOverTime(models.Model):
    _inherit = 'hr.overtime'

    payslip_id = fields.Many2one('hr.payslip')

