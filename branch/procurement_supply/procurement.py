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
import openerp.addons.decimal_precision as dp

class procurement_order(osv.osv):
    _inherit = "procurement.order"
    
    _columns = {
            'supply_partner_id': fields.many2one('res.partner', 'Supplier', domain=[('supplier','=',True)], readonly=True, states={'draft': [('readonly', False)]}),
            'supply_pricelist_id': fields.many2one('product.pricelist', 'Price List', domain=[('type','=','purchase')], readonly=True, states={'draft': [('readonly', False)]}),
            'supply_price_unit': fields.float('Unit Price', digits_compute= dp.get_precision('Product Price'), readonly=True, states={'draft': [('readonly', False)]}),
            'supply_discount': fields.float('Discount (%)', digits_compute= dp.get_precision('Discount'), readonly=True, states={'draft': [('readonly', False)]}),
            'supply': fields.boolean('Supply', readonly=True, help="Check this if the procurement is supply to avoid"),
        }
    _defaults = {
            'supply': False,
        }
    
    def action_supply(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'supply': True}, context=context)