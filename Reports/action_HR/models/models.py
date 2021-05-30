# -*- coding: utf-8 -*-
from odoo import models, fields, api


class action_HR(models.Model):
    _inherit = 'hr.employee'

    address_name = fields.Char(string='Address')

    
