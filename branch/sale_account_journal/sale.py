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

class sale_order(osv.Model):
    _inherit = 'sale.order'
    _columns = {
            'account_sale_journal_id': fields.many2one('account.journal', string="Sale Account Journal"),
        }
    
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order,self)._prepare_invoice(cr,uid,order,lines,context=context)
        if order.partner_id.property_account_sale_journal:
            res['journal_id'] = order.account_sale_journal_id.id
        return res
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = super(sale_order,self).onchange_partner_id(cr,uid,ids,part,context=context)
        if not part:
            return res
        partner = self.pool.get('res.partner').browse(cr,uid,part,context=context)
        res['value']['account_sale_journal_id'] = partner.property_account_sale_journal.id 
        return res
    
    def onchange_shop_id(self, cr, uid, ids, shop_id, context=None):
        res = super(sale_order,self).onchange_shop_id(cr, uid, ids, shop_id, context=context)
        if shop_id:
            res['value']['company_id'] = self.pool.get('sale.shop').browse(cr, uid, shop_id, context=context).company_id.id 
        return res