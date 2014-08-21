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
    
    def _get_preinvoice_copy_defaults(self, cr, uid, preline, context=None):
        res = super(sale_order,self)._get_preinvoice_copy_defaults(cr, uid, preline, context=context)
        res['name'] = preline.name + " [%s %s (%s)]"%(preline.invoice_id.internal_number or '', preline.invoice_id.date_invoice or '', preline.invoice_id.state)
        return res