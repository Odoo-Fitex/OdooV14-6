# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

    
class SaleDying(models.Model):
    _inherit = 'sale.order.line'

#     sale_order_id = fields.Many2one('sale.order.line')
#     order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    weight = fields.Char(string="M^2_Weight")
    width = fields.Char(string="Width")
    gouge = fields.Char(string="Gouge")
    inch = fields.Char(string="Inch")
    tagheez = fields.Selection([('closed', 'مقفول'), ('opened', 'مفتوح')], string='tagheez')
    al_wazn = fields.Float(string="al_wazn")
    al_3rd = fields.Float(string="al_3rd")
    al_resala = fields.Integer(string="al_resala")
    tasbeet_7rary = fields.Boolean(string="tasbeet_7rary")
    carbon = fields.Boolean(string="Carbon")
    mo3alget_zyoot = fields.Boolean(string="mo3alget_zyoot")
    us_barasel = fields.Boolean(string="us_barasel")
    tasmeegh = fields.Boolean(string="tasmeegh")
    alb_kham = fields.Boolean(string="alb_kham")
    tagheez_compactor = fields.Boolean(string="tagheez_compactor")
    kastaraa = fields.Boolean(string='kastaraa')
#     ebretan = fields.Boolean(string='ebretan')
    dye_type = fields.Selection([
        ('cotton', 'قطن/فسكوز(مرحلة واحدة)'),
        ('mixed', 'صباغة مخلوط(مرحلتين)'),
        ('polyester', 'بولييستر(مرحلة واحدة)')], string='no3 elseba8a')
    enzeem = fields.Selection([
        ('once', 'مرة'),
        ('twice', 'مرتين'),
        ('without', 'بدون')], string='enzeem')
    t7deer_7reemy_w_regaly = fields.Selection([
        ('regaly', 'تجهيز حريمي'),
        ('7reemy', 'تجهيز رجالي'),
        ('ayna', 'تجهيز مثل عينة'),
        ('ebretan', 'تجهيز ابريتان')], string='t7deer_7reemy_w_regaly')
    sakhawa = fields.Selection([
        ('sakhawa_3adya', 'سخاوة عادية'),
        ('sakhawa_3alya', 'سخاوة عالية'),
        ('sakhawa_silicon', 'سخاوة ميكروسليكونية')], string='sakhawa')

# class ActionDyingSaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
    
#     dying_ids = fields.One2many('sale.dying', 'sale_order_id')
    fabric_type_line = fields.Selection(related='order_id.fabric_type', string="Type", store=True, readonly=True)
    
#         for line in self.order_line:    
    def action_show_dye_so(self):
        view = self.env.ref('action_dying_SO.view_dying_SO_id')

        if self.display_type == 'line_section':
            return {
                'name': _('Dying Specification'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'sale.order.line',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': self.id,
            }
