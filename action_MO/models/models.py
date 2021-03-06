# -*- coding: utf-8 -*-
from odoo import models, fields, api
  
 
class action_SO_line(models.Model): 
    _inherit = 'mrp.production' 
 
    inch = fields.Char(string="Inch")
    weight = fields.Char(string="m^2_Weight")
    gouge = fields.Integer(string="Gouge")
    width = fields.Char(string="Width") 
    barcode = fields.Char(string='Barcode',
                          store=True,
                          related='product_id.barcode')
    lot_id = fields.Many2one(string='Lot/Serial Number',
                      store=True,
                      readonly=True,       
                      related='finished_move_line_ids.lot_id')
    workcenter_number = fields.Many2one('mrp.workcenter',string="Workcenter Number")
    remaining_qty = fields.Float(string="Remaining Quantity To Produce", compute="_compute_the_produced_quantity")
    total_qty_done = fields.Float(string="Quantity Partially Produced", compute="_compute_the_produced_quantity")
    actual_order_qty = fields.Float(string="Actual Quantity")
    notes = fields.Char(string="Notes")
#     customer = fields.Many2one(string="Customer", related="origin.partner_invoice_id")
    
    def my_button_mark_as_done(self):
        self.ensure_one()
        self._check_company()
        for wo in self.workorder_ids:
            if wo.time_ids.filtered(lambda x: (not x.date_end) and (x.loss_type in ('productive', 'performance'))):
                raise UserError(_('Work order %s is still running') % wo.name)
        self._check_lots()

        self.post_inventory()
        # Moves without quantity done are not posted => set them as done instead of canceling. In
        # case the user edits the MO later on and sets some consumed quantity on those, we do not
        # want the move lines to be canceled.
        (self.move_raw_ids | self.move_finished_ids).filtered(lambda x: x.state not in ('done', 'cancel')).write({
            'state': 'done',
            'product_uom_qty': 0.0,
        })
        return self.write({'state': 'done'})
        return self.write({'date_finished': fields.Datetime.now()})
    def Manufactring_order_edit(self):
     self.write({'state': 'draft'})
        

    
    @api.depends('finished_move_line_ids.qty_done')
    def _compute_the_produced_quantity(self):
        for mrp in self:
            mrp.total_qty_done = 0
            if mrp.finished_move_line_ids:
                for line in mrp.finished_move_line_ids:
                    mrp.total_qty_done += line.qty_done
                mrp.remaining_qty = mrp.actual_order_qty - mrp.total_qty_done
            else:
                 mrp.remaining_qty = 0.0
  

class action_SO_line(models.Model):
    _inherit = 'mrp.workorder'

    notes = fields.Char(string="Notes")
    date_planned_start = fields.Datetime(
        'Scheduled Date Start',
        compute='_compute_dates_planned',
        inverse='_set_dates_planned',
        states={'done': [('readonly', False)], 'cancel': [('readonly', False)]},
        store=True,
        tracking=True)
    date_planned_finished = fields.Datetime(
        'Scheduled Date Finished',
        compute='_compute_dates_planned',
        inverse='_set_dates_planned',
        states={'done': [('readonly', False)], 'cancel': [('readonly', False)]},
        store=True,
        tracking=True)
    date_start = fields.Datetime(
        'Effective Start Date',
        states={'done': [('readonly', False)], 'cancel': [('readonly', False)]})
    date_finished = fields.Datetime(
        'Effective End Date',
        states={'done': [('readonly', False)], 'cancel': [('readonly', False)]})
    qty_produced = fields.Float(
        'Quantity', default=0.0,
        readonly=False,
        digits='Product Unit of Measure',
        help="The number of products already handled by this work order")
    qty_production_wo = fields.Float('Original Production Quantity Wo', readonly=False)
    
    def Work_order_edit(self):
     self.write({'state': 'ready'})
    
class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"
     
    duration = fields.Float('Duration', compute='_compute_duration', store=True, readonly=False)
    @api.depends('date_end', 'date_start')
    def _compute_duration(self):
        for blocktime in self:
            if blocktime.date_end:
                d1 = fields.Datetime.from_string(blocktime.date_start)
                d2 = fields.Datetime.from_string(blocktime.date_end)
                diff = d2 - d1
                if (blocktime.loss_type not in ('productive', 'performance')) and blocktime.workcenter_id.resource_calendar_id:
                    r = blocktime.workcenter_id._get_work_days_data(d1, d2)['hours']
                    blocktime.duration = 1440
                else:
                    blocktime.duration = 1440
            else:
                blocktime.duration = 0.0
   
class SalesOrderAccessFromMO(models.Model):
    _inherit = 'mrp.production'
    
    origin = fields.Many2one('sale.order', 'Source',
                            states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                            help="Reference of the document that generated this production order request.")
    
    fabric_type = fields.Selection([('open','Open'),
                                    ('closed','Closed')], string="Fabric Type")
    
    slit_line = fields.Selection([('yes','Yes'),
                                   ('no','No'),
                                   ('pique','Pique Selvadge')], string="Slit Line")
    needles = fields.Integer(related='workcenter_number.needle',string="Number Of Needles", store=True)
#     SalesOrder = fields.Many2one('sale.order', 'Source')
#     customer = fields.Many2one(related='SalesOrder.partner_id', string='Customer', readonly=True)
class MRPWorkCenter(models.Model):
    _inherit = 'mrp.workcenter'
    needle =  fields.Integer(string="Number Of Needles" ,store=True)
    
class BOMAddedFields(models.Model):
    _inherit = 'mrp.bom.line'
    stitch =  fields.Float(string="Stitch Length")
   
class action_SO_line(models.Model):
    _inherit = 'mrp.production'
    workcenter2 = fields.Many2one('mrp.workcenter')
class BOMAddedFieldsManufacturingOrder(models.Model):
    _inherit = 'stock.move'
    stitch = fields.Float(string='Stitch Length',
                         store=True,
                         related='bom_line_id.stitch')
    needle = fields.Integer(string='Number Of Needles',
                            store=True,
                            related='raw_material_production_id.needles')
    yarn_lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id)]")
    MeterPerRev = fields.Float(string="Meter Per Rev", digits = (12,4), compute="compute_MeterPerRev_count")
    @api.depends('stitch','needle')
    def compute_MeterPerRev_count(self):
     for rec in self:
      rec.MeterPerRev = (rec.stitch * rec.needle)/1000
