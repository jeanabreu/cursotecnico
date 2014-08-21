# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#     Copyright (C) 2013 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta

class stock_serial(osv.Model):
    
    def _get_last_location_ids(self, cr, uid, ids, field_name, arg, context=None):
        if context is None: context = {}
        vals = {}
        for serial in self.browse(cr,uid,ids,context=context):
            vals[serial.id] = {'last_location_id': False, 'prodlot_id': False, 'tracking_id': False}
            virtual = False
            max_date = datetime(1,1,1)
            for move in serial.move_ids:
                move_date = datetime.strptime(move.date,'%Y-%m-%d %H:%M:%S')
                if move_date > max_date:
                    if move.state == 'done':
                        vals[serial.id]['last_location_id'] = move.location_dest_id.id
                    elif move.state not in ('cancel','draft'):
                        virtual = move.location_dest_id.id
                    max_date = move_date
                if move.prodlot_id:
                    vals[serial.id]['prodlot_id'] = move.prodlot_id.id
                if move.tracking_id:
                    vals[serial.id]['tracking_id'] = move.tracking_id.id
            if not vals[serial.id].get('last_location_id'): 
                vals[serial.id]['last_location_id'] = virtual
        return vals
    
    def _get_warranty_end(self, cr, uid, ids, field_name, arg, context=None):
        if context is None: context = {}
        vals = {}
        for serial in self.browse(cr,uid,ids,context=context):
            if serial.warranty_start:
                start = serial.warranty_start
                warranty = serial.warranty
                vals[serial.id] = self.get_warranty_end(start,warranty)
            else:
                vals[serial.id] = False
        return vals
    
    def _serial_from_move(self, cr, uid, ids, context=None):
        res = {}
        move_ids = self.pool.get('stock.move').browse(cr, uid, ids, context=context)
        for move in move_ids:
            for serial in move.serial_ids:
                res[serial.id] = True
        return res.keys()
    
    _name = "stock.serial"
    _columns = {
            'product_id' : fields.many2one('product.product','Product',required=True,select=1, domain=[('is_serial','=',True)]),
            'move_ids' : fields.many2many('stock.move', 'stock_serial_move_rel', 'serial_id','move_id', 'Stock moves', readonly=True),
            'prodlot_id' : fields.function(_get_last_location_ids, type='many2one', relation='stock.production.lot', string='Production Lot',
                                           store={'stock.move':(_serial_from_move,['serial_ids','prodlot_id'],10)}, multi="serial_move", select=True),
            'tracking_id' : fields.function(_get_last_location_ids, type="many2one", relation='stock.tracking', string='Tracking Number',
                                            store={'stock.move':(_serial_from_move,['serial_ids','tracking_id'],10)}, multi="serial_move", select=True),
            'name' : fields.char('Serial Number', size=64, required=True),
            'warranty' : fields.float('Warranty time (months)'),
            'warranty_start' : fields.date('Warranty Start'),
            'warranty_end' : fields.function(_get_warranty_end,string='Warranty End',type="date",method=True),
            'last_location_id' : fields.function(_get_last_location_ids,string='Last Location', type="many2one",relation="stock.location",
                                                 store={'stock.move':(_serial_from_move,['serial_ids','state',
                                                                                         'location_dest_id','location_id'],10)}, multi="serial_move", select=True),
            'uom_id' : fields.related('product_id','uom_id',type='many2one',relation='product.uom',string='Unit of Measure', store=True, readonly=True),
        }

    _defaults = {
            'warranty_start' : lambda *a: datetime.now().strftime('%Y-%m-%d'),
            'product_id' : lambda s,cr,u,c: c.get('product_id',False),
            'prodlot_id' : lambda s,cr,u,c: c.get('prodlot_id',False),
            'tracking_id' : lambda s,cr,u,c: c.get('tracking_id',False),
            'name' : '/',
        }
    _sql_contraints = [
            ('name_unique','unique(name)','The serial number must be Unique!'),
        ]

    def create(self, cr, uid, vals, context=None):
        if vals.get('name') == '/':
            product = self.pool.get('product.product').browse(cr, uid, vals.get('product_id'), context=context)
            if product.serial_sequence_id:
                vals['name'] = self.pool.get("ir.sequence").next_by_id(cr, uid, product.serial_sequence_id.id, context=context)
            else:
                vals['name'] = self.pool.get("ir.sequence").next_by_code(cr, uid, 'stock.serial', context=context)
        return super(stock_serial, self).create(cr, uid, vals, context=context)

    def on_change_product_id(self, cr, uid, ids, prod_id=False, context=None):
        if not prod_id:
            return {}

        product = self.pool.get('product.product').browse(cr, uid, prod_id, context=context)
        warranty  = product.warranty
        start = datetime.now().strftime('%Y-%m-%d')
        
        result = {
            #'prodlot_id': False,
            'warranty': warranty,
            #'move_ids': False,
            'warranty_start' : start,
            'warranty_end': self.get_warranty_end(start,warranty),
        }
        
        return {'value': result}
    
    def on_change_warranty(self, cr, uid, ids, start, warranty, context=None):
        if not start:
            return {}
        
        result = {
            'warranty_end': self.get_warranty_end(start,warranty),
        }
        
        return {'value': result}
    
    def get_warranty_end(self,start,months):
        if not start: return False
        limit = datetime.strptime(start,'%Y-%m-%d') + relativedelta(months=int(months))
        return limit.strftime('%Y-%m-%d')
