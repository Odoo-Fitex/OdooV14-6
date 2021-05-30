# -*- coding: utf-8 -*-

from odoo import models, fields, api


class action_payroll(models.Model):
    _inherit = 'hr.payslip'


    overtime_1 = fields.Float(string="OverTime(Night Shift)")
    overtime_2 = fields.Float(string="OverTime(Day Shift)")
    bonus = fields.Float(string="Bonus")
    incentive = fields.Float(string="Incentive")
    adjustment_1 = fields.Float(string="Additional Adjustment")
    absence_with_per = fields.Float(string="Absence With Permission")
    absence_without_per = fields.Float(string="Absence Without Permission")
    penality = fields.Float(string="Penality")
    latency1 = fields.Float(string="Latency 1")
    adjustment_2 = fields.Float(string="Deduction Adjustment")
    other = fields.Float(string="Other Deduction")


    