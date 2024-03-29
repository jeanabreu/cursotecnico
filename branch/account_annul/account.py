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

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    
    _columns = {
        'state': fields.selection([
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('annul','Anulled'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
            ],'Status', select=True, readonly=True, track_visibility='onchange',
            help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Invoice. \
            \n* The \'Pro-forma\' when invoice is in Pro-forma status,invoice does not have an invoice number. \
            \n* The \'Open\' status is used when user create invoice,a invoice number is generated.Its in open status till user does not pay invoice. \
            \n* The \'Paid\' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled. \
            \n* The \'Anulled\' status is used when user annul invoice (keeping the invoice number).\
            \n* The \'Cancelled\' status is used when user cancel invoice.'),
        }
    
    def action_annul(self, cr, uid, ids, context=None):
        move_ids = [i.move_id.id for i in self.browse(cr, uid, ids, context=context)]
        self.write(cr, uid, ids, {'state': 'annul'}, context=context)
        return self.pool.get('account.move').button_annul(cr, uid, move_ids, context=context)
    

class account_move(osv.Model):
    _inherit = 'account.move'

    _columns = {
            'annul': fields.boolean('Annulled', readonly=True),
        }
    
    def button_annul(self, cr, uid, ids, context=None):
        if context is None: context={}
        line_ids = []
        self.button_cancel(cr, uid, ids, context=context)
        for move in self.browse(cr, uid, ids, context=context):
            for line in move.line_id:
                line_ids.append(line.id)
        self.write(cr, uid, ids, {'annul': True}, context)
        return self.pool.get('account.move.line').unlink(cr, uid, line_ids, context=context)