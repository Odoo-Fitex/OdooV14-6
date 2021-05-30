# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # for addition
    Performance_incentive = fields.Float(string="Performance Incentive")
    reward = fields.Float(string="Reward")
    approved_hours_overtime = fields.Float(string="Approved Hours Overtime", compute='approved_overtime')
    approved_days_overtime = fields.Float(string="Approved Days Overtime", compute='approved_overtime')
    other_benefits = fields.Float(string="Other Benefits")
    # for deduction
    no_permission_absence_penalty = fields.Float(string="No Permission Absence Penalty")
    no_finger_print_penalty = fields.Float(string="No Finger Print Penalty")
    penalties = fields.Float(string="Penalties")
    other_discount = fields.Float(string="Other Discount")

    @api.depends('employee_overtime_ids', 'employee_overtime_ids.days_no_tmp')
    def approved_overtime(self):
        for rec in self:
            if rec.employee_overtime_ids:
                hours = 0.0
                days = 0.0
                for line in rec.employee_overtime_ids:
                    if line.duration_type == 'hours':
                        hours += line.days_no_tmp
                    if line.duration_type == 'days':
                        days += line.days_no_tmp
                rec.approved_hours_overtime = hours
                rec.approved_days_overtime = days
            else:
                rec.approved_hours_overtime = 0.0
                rec.approved_days_overtime = 0.0



