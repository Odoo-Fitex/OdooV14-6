# -*- coding: utf-8 -*-

from odoo import models, fields, api
   
 
class MrpProduction(models.Model): 
    _inherit = 'mrp.production' 

    color_bom_id = fields.Many2one('mrp.bom')# for dying
    chemical_bom_id = fields.Many2one('mrp.bom')# for chemical
    color_bom_line_ids = fields.Many2many('mrp.bom.line')
    production_bom_line_ids = fields.Many2many('production.bom.line')# for dying
    chemical_production_bom_line_ids = fields.Many2many('chemical.production.bom.line')# for chemical
    liqur_ratio = fields.Float(string="Liqur Ratio")
    liqur_ratio_2 = fields.Float(string="Liqur Ratio")
    dying_mo = fields.Boolean(string="Is Dying MO", default=False)#to specify if it's a dying mo
    
                                                                     #for dyed MO specification
    
    grey_weight = fields.Float(string="Greige_M^2_Weight")
    grey_width = fields.Float(string="Greige_Width")
    raising =  fields.Selection([
                                    ('yes', 'Yes'),
                                    ('no', 'No')], string='Raising')
    
    carbon =  fields.Selection([
                                    ('yes', 'Yes'),
                                    ('no', 'No')], string='Carbon')
    
    compactor =  fields.Selection([
                                    ('yes', 'Yes'),
                                    ('no', 'No')], string='Compactor')
    gluing =  fields.Selection([
                                    ('yes', 'Yes'),
                                    ('no', 'No')], string='Gluing')
    cutting_selvadge =  fields.Selection([
                                            ('yes', 'Yes'),
                                            ('no', 'No')], string='Cutting Selvadge')
    heat_setting =  fields.Selection([
                                        ('yes', 'Yes'),
                                        ('no', 'No')], string='Heat Setting')
    oil_removing =  fields.Selection([
                                        ('yes', 'Yes'),
                                        ('no', 'No')], string='Oil Removing')
    enzyme =  fields.Selection([
                                    ('no', 'No'),
                                    ('single', 'Single'),
                                    ('double', 'Double')], string='Enzyme')
    

                                                                     # for dying tab
        
    @api.onchange('color_bom_id')
    def onchange_production_bom_load_lines(self):
        if self.color_bom_id:
            print("Hello color bom lines")
            print(self.color_bom_id.bom_line_ids)
            self.write({'production_bom_line_ids': [(2, tag.id, 0) for tag in self.mapped('production_bom_line_ids')]})
            self.write(
                {'production_bom_line_ids': [(0, 0, {'product_id': line.product_id.id, 'product_qty': line.product_qty,
                                                     'percentage': line.percentage, 'product_uom_id': line.product_uom_id,
                                                     'original_bom_line_id': line.id})
                                             for line in self.color_bom_id.bom_line_ids]})

                                                                     # for chemicals tab
                
# for chemicals tab
    @api.onchange('chemical_bom_id')
    def onchange_chemical_production_bom_load_lines(self):
        if self.chemical_bom_id:
            print("Hello chemicals bom lines")
            print(self.chemical_bom_id.bom_line_ids)
            self.write(
                {'chemical_production_bom_line_ids': [(2, tag.id, 0) for tag in self.mapped('chemical_production_bom_line_ids')]})
            self.write(
                {'chemical_production_bom_line_ids': [
                    (0, 0, {'product_id': line.product_id.id, 'product_qty': line.product_qty,
                            'percentage': line.percentage, 'product_uom_id': line.product_uom_id,
                            'original_bom_line_id': line.id})
                    for line in self.chemical_bom_id.bom_line_ids]})





#     @api.onchange('color_bom_id')
#     def onchange_color_bom_load_lines(self):
#         if self.color_bom_id:
#             print("Hello color bom lines")
#             print(self.color_bom_id.bom_line_ids)
#             self.write({'color_bom_line_ids': [(0, 0, {'product_id': line.product_id.id, 'product_qty': line.product_qty,
#                                                        'original_bom_line_id': line.id, 'bom_id': 0})
#                                                for line in self.color_bom_id.bom_line_ids]})
#     #
    def compute_color_bom_line_quantity(self):
        if self.color_bom_id:
            if self.color_bom_id.material_type == 'chemicals':
                if self.production_bom_line_ids:
                    for line in self.production_bom_line_ids:
                        line.product_qty = self.product_qty * self.liqur_ratio * line.percentage / 100
                        # for update components of MO
                        for component in self.move_raw_ids:
                            if component.bom_line_id.id == line.original_bom_line_id.id:
                                component.product_uom_qty = line.product_qty
            if self.color_bom_id.material_type == 'dyed':
                if self.production_bom_line_ids:
                    for line in self.production_bom_line_ids:
                        line.product_qty = self.product_qty * line.percentage / 100
                        # for update components of MO
                        for component in self.move_raw_ids:
                            if component.bom_line_id.id == line.original_bom_line_id.id:
                                component.product_uom_qty = line.product_qty

    def compute_color_bom_line_quantity_chemicals(self):
        if self.chemical_bom_id:
            if self.chemical_bom_id.material_type == 'chemicals':
                if self.chemical_production_bom_line_ids:
                    for line in self.chemical_production_bom_line_ids:
                        line.product_qty = self.product_qty * self.liqur_ratio_2 * line.percentage
                        # for update components of MO
                        for component in self.move_raw_ids:
                            if component.bom_line_id.id == line.original_bom_line_id.id:
                                component.product_uom_qty = line.product_qty







    # def _compute_color_bom_line_quantity(self):
    #     if self.color_bom_id:
    #         if self.color_bom_id.material_type == 'chemicals':
    #             if self.color_bom_line_ids:
    #                 for line in self.color_bom_line_ids:
    #                     line.product_qty = self.color_bom_id.product_qty * self.liqur_ratio * line.percentage / 100
    #         elif self.color_bom_id.material_type == 'dyed':
    #             if self.color_bom_line_ids:
    #                 for line in self.color_bom_line_ids:
    #                     line.product_qty = self.color_bom_id.product_qty * line.percentage / 100

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    original_bom_line_id = fields.Many2one('mrp.bom.line')


class ProductionBomLine(models.Model):
    _name = 'production.bom.line'

    product_id = fields.Many2one('product.product', string="Component")
    percentage = fields.Float(string="Percentage", digits=(11, 4))
    product_qty = fields.Float(string="Quantity", digits=(11, 3))
    product_uom_id = fields.Many2one('uom.uom', string="Product UOM")
    original_bom_line_id = fields.Many2one('mrp.bom.line')


class ChemicalProductionBomLine(models.Model):
    _name = 'chemical.production.bom.line'

    product_id = fields.Many2one('product.product', string="Component")
    percentage = fields.Float(string="Percentage", digits=(11, 4))
    product_qty = fields.Float(string="Quantity", digits=(11, 3))
    product_uom_id = fields.Many2one('uom.uom', string="Product UOM")
    original_bom_line_id = fields.Many2one('mrp.bom.line')
