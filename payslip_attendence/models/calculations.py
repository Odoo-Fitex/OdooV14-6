# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    month_days = fields.Float(string="Month Days", default=26)                          # Day
    attendance_days = fields.Float(string="Attendance Days")                            # code=100
    finger_print_attendance_days = fields.Float(string="Finger Attendance Days", compute='compute_late_singout_hours')
    total_late_hours = fields.Float(string="Total Late Hours", compute='compute_late_singout_hours')
    total_sign_out_hours = fields.Float(string="Total SignOut Hours", compute='compute_late_singout_hours')
    absence_without_permission = fields.Float(string="Absence Without Permission", compute='compute_absence_without_permission')
    over_days = fields.Float(string="Over Days", compute='compute_absence_without_permission')
    compute_late_hours = fields.Float(string="Compute Late Hours", compute='compute_net_late_hours')
    compute_sign_out_hours = fields.Float(string="Compute SignOut Hours", compute='compute_net_late_hours')
    net_late_hours = fields.Float(string="Net Late Hours", compute='compute_net_late_hours')

    annual_vacation_2020 = fields.Float(string="Annual Vacation 2020")                  # code=101
    annual_vacation_2019 = fields.Float(string="Annual Vacation 2019")                  # code=102
    rest_allowance = fields.Float(string="Rest Allowance")                              # code=103
    days_mission = fields.Float(string="Days Mission")                                  # code=104
    hours_mission = fields.Float(string="Hours Mission")                                # code=116
    late_permission = fields.Float(string="Late Permission")                            # code=105
    early_sign_out = fields.Float(string="Early Sign Out")                              # code=106
    sick_leave_100 = fields.Float(string="Sick Leave 100%")                             # code=107
    sick_leave_70 = fields.Float(string="Sick Leave 70%")                               # code=108
    without_balance_leave = fields.Float(string="Without Balance Leave")                # code=109
    death_leave = fields.Float(string="Death Leave")                                    # code=110
    maternity_leave = fields.Float(string="Maternity Leave")                            # code=111
    haj_omra_leave = fields.Float(string="Haj Omra Leave")                              # code=112
    work_injury = fields.Float(string="Work Injury")                                    # code=113
    health_insurance_permission = fields.Float(string="Health Insurance Permission")    # code=114
    exile_permission = fields.Float(string="Exile Permission")                          # code=115
    marriage_vacation = fields.Float(string="Marriage Vacation")                        # code=117
    car_late_permission = fields.Float(string="Car Late Permission")                    # code=118

    def calculate_action(self):
        # validation
        # calculate value for fields
        for worked in self.worked_days_line_ids:
            if worked.code == '100':
                self.attendance_days = worked.number_of_days
            elif worked.code == '101':
                self.annual_vacation_2020 = worked.number_of_days
            elif worked.code == '102':
                self.annual_vacation_2019 = worked.number_of_days
            elif worked.code == '103':
                self.rest_allowance = worked.number_of_days
            elif worked.code == '104':
                self.days_mission = worked.number_of_days
            elif worked.code == '105':
                self.late_permission = worked.number_of_hours
            elif worked.code == '106':
                self.early_sign_out = worked.number_of_hours
            elif worked.code == '107':
                self.sick_leave_100 = worked.number_of_days
            elif worked.code == '108':
                self.sick_leave_70 = worked.number_of_days
            elif worked.code == '109':
                self.without_balance_leave = worked.number_of_days
            elif worked.code == '110':
                self.death_leave = worked.number_of_days
            elif worked.code == '111':
                self.maternity_leave = worked.number_of_days
            elif worked.code == '112':
                self.haj_omra_leave = worked.number_of_days
            elif worked.code == '113':
                self.work_injury = worked.number_of_days
            elif worked.code == '114':
                self.health_insurance_permission = worked.number_of_hours
            elif worked.code == '115':
                self.exile_permission = worked.number_of_hours
            elif worked.code == '117':
                self.marriage_vacation = worked.number_of_days
            elif worked.code == '116':
                self.hours_mission = worked.number_of_hours
            elif worked.code == '118':
                self.car_late_permission = worked.number_of_hours

    def compute_late_singout_hours(self):
        for rec in self:
            if rec.employee_attendance_ids:
                total_late_hours = 0.0
                total_sign_out_hours = 0.0
                for line in rec.employee_attendance_ids:
                    total_late_hours += line.late
                    total_sign_out_hours += line.early_leave
                rec.total_late_hours = total_late_hours
                rec.total_sign_out_hours = total_sign_out_hours
                rec.finger_print_attendance_days = len(rec.employee_attendance_ids)
            else:
                rec.total_late_hours = 0.0
                rec.total_sign_out_hours = 0.0
                rec.finger_print_attendance_days = 0.0

    def compute_absence_without_permission(self):
        for rec in self:
            other_days = rec.annual_vacation_2020 + rec.annual_vacation_2019 \
                         + rec.rest_allowance + rec.days_mission + rec.sick_leave_100 + rec.sick_leave_70 \
                         + rec.without_balance_leave + rec.death_leave + rec.maternity_leave + rec.haj_omra_leave\
                         + rec.work_injury + rec.marriage_vacation
            if rec.finger_print_attendance_days >= rec.month_days:
                rec.over_days = rec.finger_print_attendance_days - rec.month_days
                rec.absence_without_permission = 0.0
            else:
                diff = rec.month_days - rec.finger_print_attendance_days
                if diff == other_days:
                    rec.absence_without_permission = 0.0
                    rec.over_days = 0.0
                if diff > other_days:
                    rec.absence_without_permission = diff - other_days
                    rec.over_days = 0.0

    def compute_net_late_hours(self):
        for rec in self:
            other_late_hours = rec.hours_mission + rec.late_permission + rec.health_insurance_permission + rec.car_late_permission
            x = rec.total_late_hours - other_late_hours
            if x > 0:
                rec.compute_late_hours = x
            else:
                rec.compute_late_hours = 0.0

            other_sign_out_hours = rec.early_sign_out + rec.exile_permission
            y = rec.total_sign_out_hours - other_sign_out_hours
            if y > 0:
                rec.compute_sign_out_hours = y
            else:
                rec.compute_sign_out_hours = 0.0

            rec.net_late_hours = rec.compute_late_hours + rec.compute_sign_out_hours




