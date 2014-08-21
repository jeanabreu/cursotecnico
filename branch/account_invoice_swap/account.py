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

class account_move_line(osv.Model):
    _inherit = 'account.move.line'
    
    def reconcile(self, cr, uid, ids, type='auto', writeoff_acc_id=False, writeoff_period_id=False, writeoff_journal_id=False, context=None):
        if context is None:
            context = {}
        lines = self.browse(cr, uid, ids, context=context)
        unrec_lines = filter(lambda x: not x['reconcile_id'], lines)
        invoice_swap = True
        for line in unrec_lines:
            if line.partner_id:
                invoice_swap = not line.partner_id.invoice_swap
                break
        context['restrict_only_one_account'] = invoice_swap
        return super(account_move_line,self).reconcile(cr, uid, ids, type=type, writeoff_acc_id=writeoff_acc_id, writeoff_period_id=writeoff_period_id, writeoff_journal_id=writeoff_journal_id, context=context)
