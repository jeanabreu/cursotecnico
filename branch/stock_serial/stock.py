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
from tools.translate import _
from openerp.osv.orm import setup_modifiers
from lxml import etree

class stock_move(osv.osv):
    
#     def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
#         res = super(stock_move, self).fields_view_get(cr, user, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
#         if res.get('type') != 'form':
#             return res
#         doc = etree.XML(res['arch'])
#         nodes = doc.xpath("//field[@name='serial_ids']")
#         for node in nodes:
#             node.set('domain',"[('tracking_id','=',tracking_id),('prodlot_id','=',prodlot_id),('product_id','=',product_id),'|',('last_location_id','=',location_id),('last_location_id','=',False)]")
#             setup_modifiers(node, res['fields']['serial_ids'])
#         res['arch'] = etree.tostring(doc)
#         return res
    
    
    def _check_quantity(self, cr, uid, ids, context=None):
        for move in self.browse(cr, uid, ids, context=context):
            if move.state not in ('draft','confirmed','assigned')  and move.product_id.is_serial and move.product_qty != len(move.serial_ids):
                return False
        return True
    
    _name = "stock.move"
    _inherit = "stock.move"
    _columns = {
            'serial_ids':fields.many2many('stock.serial', 'stock_serial_move_rel','move_id', 'serial_id', 'Serial numbers',states={'done': [('readonly', True)]}),
            'is_serial':fields.related('product_id','is_serial',type='boolean', store=True),
        }
    _constraints = [
            (_check_quantity,'The product quentity must be equal to serial numbers count',['product_qty','serial_ids']),
        ]
    
    def create_serials(self, cr, uid, ids, context=None):
        for move in self.browse(cr,uid,ids):
            if move.product_id.is_serial:
                for i in range (0,move.product_qty):
                    vals =  {
                         'move_ids':[(6, 0, [move.id])]
                    }
                    context={
                        'product_id':move.product_id.id,
                        'prodlot_id' : move.prodlot_id and move.prodlot_id.id or False,
                        'tracking_id' : move.tracking_id and move.tracking_id.id or False,
                    }
                    self.pool.get('stock.serial').create(cr,uid,vals ,context)

    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False,
                            loc_dest_id=False, partner_id=False):
        res = {}
        res = super(stock_move, self).onchange_product_id(cr, uid, ids, prod_id=prod_id, loc_id=loc_id, loc_dest_id=loc_dest_id, partner_id=partner_id)
        if not prod_id:
            return res
        product = self.pool.get('product.product').browse(cr, uid, prod_id)
        res['value']['is_serial'] = product.is_serial
        return res

    def onchange_serial_ids(self, cr, uid, ids, serial_ids):
        res = {'value':{}}
        res['value']['product_qty'] = len(serial_ids[0][2])
            
        return res

#     def write(self, cr, uid, ids, vals, context=None):
#         if 'product_qty' in vals or 'serial_ids' in vals:
#             if 'product_qty' in vals:
#                 qty = vals['product_qty']
#             else:
#                 qty = self.pool.get('stock.move').browse(cr, uid, ids[0]).product_qty
#             if 'serial_ids' in vals:
#                 len_serial = len(vals['serial_ids'][0][2])
#             else:
#                 len_serial = len(self.pool.get('stock.move').browse(cr, uid, ids[0]).serial_ids)
#                 
#             if qty != len_serial:
#                 raise osv.except_osv(_('Error'),
#                                 _('The quantity is not equal to serial numbers'))
#         return  super(stock_move, self).write(cr, uid, ids, vals, context=context)


class stock_production_lot(osv.osv):
    _name = "stock.production.lot"
    _inherit = "stock.production.lot"
    _columns = {
        'serial_ids':fields.one2many('stock.serial', 'prodlot_id',string='Serial numbers', readonly=True),
    }


class stock_tracking(osv.osv):
    _name = "stock.tracking"
    _inherit = "stock.tracking"
    _columns = {
        'serial_ids':fields.one2many('stock.serial', 'tracking_id',string='Serial numbers', readonly=True),
    }
