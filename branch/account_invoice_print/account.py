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

class account_journal(osv.Model):
    _inherit = 'account.journal'
    _columns = {
            'invoice_report_id': fields.many2one('ir.actions.report.xml', string="Report Invoice", 
                                         domain=[('model','=','account.invoice')], 
                                         help="This report is used on invoice print button"),
        }

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    
    def invoice_print(self, cr, uid, ids, context=None):
        res = super(account_invoice,self).invoice_print(cr, uid, ids, context=context)
        account = self.browse(cr, uid, ids[0], context=context)
        if account.journal_id.invoice_report_id:
            res['report_name'] = account.journal_id.invoice_report_id.report_name 
        return res
    


    