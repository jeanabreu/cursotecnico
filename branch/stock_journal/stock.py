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

from openerp.osv import osv, fields

class stock_journal(osv.osv):
    _name = "stock.journal"
    _inherit = 'stock.journal'
    _columns = {
            'sequence_id': fields.many2one('ir.sequence','Sequence'),
            'warehouse_id': fields.many2one('stock.warehouse','Warehouse', ),
        }

class stock_picking_in(osv.Model):
    _name = "stock.picking.in"
    _inherit = "stock.picking.in"
    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = '\\'
        new_id = super(stock_picking_in, self).create(cr, user, vals, context)
        if vals.get('name', False) == '\\':
            self.write(cr, user, [new_id], {'name':'/'}, context=context)
        return new_id

class stock_picking_out(osv.Model):
    _name = "stock.picking.out"
    _inherit = "stock.picking.out"
    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = '\\'
        new_id = super(stock_picking_out, self).create(cr, user, vals, context)
        if vals.get('name', False) == '\\':
            self.write(cr, user, [new_id], {'name':'/'}, context=context)
        return new_id
    
class stock_picking(osv.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = '\\'
        new_id = super(stock_picking, self).create(cr, user, vals, context)
        if vals.get('name', False) == '\\':
            self.write(cr, user, [new_id], {'name':'/'}, context=context)
        return new_id

    def action_assign_wkf(self, cr, uid, ids, context=None):
        
        for picking in self.browse(cr, uid, ids, context=context):
            res = {}
            if picking.name or picking.name == '/':
                if picking.stock_journal_id and picking.stock_journal_id.sequence_id:
                    res['name'] = self.pool.get('ir.sequence').get_id(cr, uid, picking.stock_journal_id.sequence_id.id)
                else:
                    seq_obj_name =  self._name
                    if picking.type != 'internal':
                        seq_obj_name += '.' + picking.type 
                    res['name'] = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)
            if res:
                self.write(cr,uid,[picking.id],res,context=context)
                
        return super(stock_picking, self).action_assign_wkf(cr, uid, ids, context=context)
        
    def _default_location_destination(self, cr, uid, context=None):
        res = super(stock_picking, self)._default_location_destination(cr, uid, context=context)
        if not res: 
            res = context.get('location_des_id', False)
        return res

    def _default_location_source(self, cr, uid, context=None):
        res = super(stock_picking, self)._default_location_source(cr, uid, context=context)
        if not res: 
            res = context.get('location_id', False)
        return res