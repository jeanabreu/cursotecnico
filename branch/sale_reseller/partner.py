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

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    _columns = {
            'reseller_id': fields.many2one('res.partner', string="Asigned Reseller", domain=[('reseller','=',True)]),
            'reseller': fields.boolean('Reseller'),
            'reseller_childs': fields.one2many('res.partner','reseller_id', string='Reseller Customers'),
        }
    _defaults = {
            'reseller': False,
        }