# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#     Copyright (C) 2014 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
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

class res_partner(osv.Model):
    
    def _partial_reconcile_amount(self, cr, uid, ids, field_names, args, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        ctx['all_fiscalyear'] = True
        query = self.pool.get('account.move.line')._query_get(cr, uid, context=ctx)
        cr.execute("""SELECT l.partner_id, a.type, SUM(l.debit-l.credit)
                      FROM account_move_line l
                      LEFT JOIN account_account a ON (l.account_id=a.id)
                      WHERE a.type IN ('receivable','payable')
                      AND l.partner_id IN %s
                      AND l.reconcile_partial_id IS NOT NULL
                      AND """ + query + """
                      GROUP BY l.partner_id, a.type
                      """,
                   (tuple(ids),))
        maps = {'receivable':'partial_credit', 'payable':'partial_debit' }
        res = {}
        for id in ids:
            res[id] = {}.fromkeys(['partial_credit','partial_debit','partial_reconcile_pending','partial_reconcile_amount'], 0)
        for pid,type,val in cr.fetchall():
            if val is None: val=0
            res[pid][maps[type]] = (type=='receivable') and val or -val
        for _id in ids:
            res[_id]['partial_reconcile_pending'] = res[_id]['partial_debit'] - res[_id]['partial_credit']
            res[_id]['partial_reconcile_amount'] = min(res[_id]['partial_debit'], res[_id]['partial_credit'])
        return res
    
    _inherit = 'res.partner'
    _columns = {
            'invoice_swap': fields.boolean('Invoice Swap', help="This check allow to reconcile supplier invoices with customer invoices of this partner"),
            'partial_credit': fields.function(_partial_reconcile_amount, string="Partial Reconcile Receivable", multi="partial_reconcile"),
            'partial_debit': fields.function(_partial_reconcile_amount, string="Partial Reconcile Payable", multi="partial_reconcile"),
            'partial_reconcile_pending': fields.function(_partial_reconcile_amount, string="Partial Reconcile Pending", multi="partial_reconcile"),
            'partial_reconcile_amount': fields.function(_partial_reconcile_amount, string="Partial Reconcile Amount", multi="partial_reconcile"),
        }
    _defaults = {
            'invoice_swap': False,
        }    