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

class pos_config(osv.osv):
    _name = "pos.config"
    _inherit = "pos.config"

    _columns = {
        'individual_accounting': fields.boolean('Individual Accounting', help="Generate individual journal entries by each POS order"),
    }
    _defaults = {
        'individual_accounting': False,
    }


class pos_session(osv.osv):
    _name = 'pos.session'
    _inherit = 'pos.session'
    
    _columns = {
        'individual_accounting': fields.related('config_id', 'individual_accounting',
                                       type='booelan',
                                       readonly=True,
                                       string='Individual Accounting'),
    }
    
    def _confirm_orders(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context=context):
            if session.individual_accounting:
                for order in session.order_ids:
                    self.pool.get('pos.order')._create_account_move_line(cr, uid, [order.id], session, context=context)
            else:
                super(pos_session,self)._confirm_orders(cr, uid, [session.id], context=context)
        
        return True

class pos_order(osv.osv):
    _name = "pos.order"
    _inherit = "pos.order"

    _columns = {
        'sale_journal': fields.many2one('account.journal', 'Sale Journal', required=True, states={'draft': [('readonly', False)]}, readonly=True),
    }
    _defaults = {
        'sale_journal': lambda s,cr,u,c:s.pool.get('pos.session').browse(cr,u,s._default_session(cr,u,c)).config_id.journal_id.id,
    }
    
    def create(self, cr, uid, values, context=None):
        if not self.pool.get('pos.session').browse(cr, uid, values['session_id'], context=context).individual_accounting: 
            values['name'] = '/'
        return super(pos_order, self).create(cr, uid, values, context=context)
    
    def create_from_ui(self, cr, uid, orders, context=None):
        #_logger.info("orders: %r", orders)
        order_ids = super(pos_order, self).create_from_ui(cr, uid, orders, context=context)
        for _order in orders:
            order = _order['data']
            order_brw = self.browse(cr , uid, self.search(cr, uid, [('id','in',order_ids),('pos_reference','=',order['name'])], context=context)[0], context=context)
            if order['number'] == '/':
                self.write(cr, uid, [order_brw.id], {
                                                 'sale_journal':order['sale_journal'],
                                                 }, context)
            else:
                self.write(cr, uid, [order_brw.id], {
                                                 'name':order['number'],
                                                 'sale_journal':order['sale_journal'],
                                                 }, context)
                self.pool.get('stock.picking').write(cr, uid, [order_brw.picking_id.id],{
                                                                                     'origin':order_brw.picking_id.origin+' / '+order['number'],
                                                                                     },context=context)
                if not order['sequence_sync']:
                    self.pool.get('ir.sequence').next_by_id(cr, uid, self.pool.get('account.journal').
                                                        browse(cr,uid,order['sale_journal'],context=context).sequence_id.id,context=context)
        return order_ids
    
    def get_account_move_create(self, cr, uid, order, context=None):
        res = super(pos_order, self).get_account_move_create(cr, uid, order, context=context)
        if order.session_id.individual_accounting:
            res['name'] = order.name
            res['ref'] = order.pos_reference
        return res