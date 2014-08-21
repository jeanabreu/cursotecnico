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
from openerp.tools.translate import _

class pos_order(osv.osv):
    _name = "pos.order"
    _inherit = "pos.order"
    
    def create_from_ui(self, cr, uid, orders, context=None):
        order_ids = super(pos_order, self).create_from_ui(cr, uid, orders, context=context)
        for _order in orders:
            order = _order['data']
            order_brw = self.browse(cr , uid, self.search(cr, uid, [('id','in',order_ids),('pos_reference','=',order['name'])], context=context)[0], context=context)
            if order['partner_id']:
                self.write(cr, uid, [order_brw.id], {
                                                 'partner_id':order['partner_id'],
                                                 }, context)
            else:
                if order['vat_number'] and order['vat_name']:
                    self.pool.get('res.partner').create(cr, uid, {
                                                                 'name':order['vat_name'],
                                                                 'ref':order['vat_number'],
                                                                 },context=context)
        return order_ids
    