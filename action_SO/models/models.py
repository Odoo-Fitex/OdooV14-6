 # -*- coding: utf-8 -*-
from odoo import models, fields, api


class action_SO(models.Model):
    _inherit = 'sale.order'  

    delivery_distination = fields.Char(string="Dye House Address")
    number_of_out = fields.Integer(string="Delivery Paper Number")
    fabric_type = fields.Selection([('Yarn','Yarn'),
                                    ('Grey','Grey'), 
                                    ('Dyed','Dyed'),
                                    ('servivce','Service')], required=True, string="Sale's Order Type")
    done = fields.Boolean(string="Fully Delivered")
    
    def sales_unlock(self):
     self.write({'state': 'sale'})
    def sales_Qoutation(self):
     self.write({'state': 'draft'})
     
    def sales_done(self):
     for order in self:
         tx = order.sudo().transaction_ids.get_last_transaction()
         if tx and tx.state == 'pending' and tx.acquirer_id.provider == 'transfer':
             tx._set_transaction_done()
             tx.write({'is_processed': True})
     return self.write({'state': 'done'})

class action_SO_line(models.Model):
    _inherit = 'sale.order.line'

    inch = fields.Char(string="Inch")
    weight = fields.Char(string="M^2_Weight")
    width = fields.Char(string="Width")
    gouge = fields.Char(string="Gouge")
    attached = fields.Char(string="Attached_MO")
    barcode = fields.Char(string='Barcode',
                          store=True,
                          related='product_id.barcode')
    attached = fields.Many2one('mrp.production', 'Attached MO')
    barcode = fields.Char(string='Barcode',
                          store=True,
                          related='product_id.barcode')
    product_uom_qty = fields.Float('Reserved',readonly= False, default=0.0, digits='Product Unit of Measure', required=True)
 


class action_WHOUT_line_move_lines(models.Model):
    _inherit = 'stock.move'
    barcode = fields.Char(string='Barcode',
                          store=True,
                          related='product_id.barcode')
    trade_name = fields.Char(string='The Trade Name',
                             store=True,
                             related='product_id.name')

    color = fields.Char(string="Color")
    rolls_number = fields.Float(string="Number Of Rolls/Boxes")
    rolls_weight = fields.Float(string="Rolls Weight")
    notes = fields.Char(string="Notes")
    lot_id = fields.Many2one(string='lot',
                             store=True,
                             related='move_line_ids.lot_id')
    
    boxes = fields.Integer(string="Boxes")
    
class action_WHOUT_stock_move_lines(models.Model):
    _inherit = 'stock.move.line'

    barcode2 = fields.Char(string='Barcode',
                           store=True,
                           related='product_id.barcode')
    trade_name2 = fields.Char(string='The Trade Name',
                              store=True,
                              related='product_id.name')
    color2 = fields.Char(string="Color")
    rolls_number2 = fields.Integer(string="Number Of Rolls/Boxes")
    notes2 = fields.Char(string="Notes")
    reserved_availability = fields.Float(
        'Quantity Reserved',
        digits='Product Unit of Measure',
        readonly=False, help='Quantity that has already been reserved for this move')
    product_uom_qty = fields.Float(
        'Initial Demand',
        digits='Product Unit of Measure',
        default=0.0, required=True,
        help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")
    
class action_SO_line(models.Model):
    _inherit = 'stock.picking'

    number_of_out = fields.Char(string="Delivery Paper Number")
    driver = fields.Char(string="Driver's Name")
    car_plate = fields.Char(string="Car Plate Number")
    driver_phone = fields.Char(string="Car Plate Number")
    delivered_by = fields.Char(string="Delivered_By")
    delivered_to = fields.Char(string="Delivered_To")
    dye_house_address = fields.Char(string="Dyehouse Address")
    delivery_fee = fields.Float(string="Delivery Fee")
    total_rolls = fields.Float(string="Total Count Of Rolls", compute="_amount_all_rolls")
    total_quantity = fields.Float(string="Total Quantity", compute="_amount_all_rolls")

      #def _amount_all_rolls(self):
      #  for stock in self:
          #  total_rolls = total_quantity = 0.0
      #  if stock.move_ids_without_package:   
            #for line in stock.move_ids_without_package:
             #   total_rolls += line.rolls_number
           #     total_quantity += line.quantity_done
            #    stock.update({
           #     'total_rolls': total_rolls,
           #     'total_quantity': total_quantity,
          #  })
      
      
    @api.depends('location_id')
    def _compute_lot_serial_number_between_operations_detailed_operations(self):
        for stock in self:
            for line in stock.move_line_ids_without_package:
                for record in stock.move_ids_without_package:
                    if line.move_id == record.move_line_ids:
                        record.lot_id == line.lot_id
          
class Picking(models.Model):
    _inherit = "stock.picking"
    
    def button_validate(self):
        res = super(Picking, self).button_validate()
        for rec in self.move_lines:
            current_number_of_boxes = rec.lot_id.roll_number
            new_number_of_boxes = current_number_of_boxes + rec.boxes
            rec.lot_id.write({'roll_number': new_number_of_boxes})
        return res

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
  
  
    READONLY_STATES = {
        'purchase': [('readonly', False)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES,
                                 change_default=True, tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
