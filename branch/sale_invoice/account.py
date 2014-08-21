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

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    _columns = {
        'sale_order_ids': fields.many2many('sale.order', 'sale_order_invoice_rel', 'invoice_id', 'order_id', 'Sale Orders', 
                                           readonly=True, states={'draft': [('readonly', False)]}, help="This is the list of sale orders related to this invoice. The same sales order may have been invoiced in several times (by line for example)."),
        }