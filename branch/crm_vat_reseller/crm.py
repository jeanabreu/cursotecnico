# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2013 Cubic ERP - Teradata SAC. (http://cubicerp.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp.osv import osv, fields

class crm_lead(osv.osv):
    
    def _check_reseller(self, cr, uid, ids, context=None):
        for lead in self.browse(cr, uid, ids, context=context):
            if lead.partner_vat:
                vals = self.pool.get('res.partner').search(cr, uid, [('company_id','=',lead.company_id.id),
                                                                     ('vat','=',lead.partner_vat),
                                                                     ('reseller_id','not in',(False,lead.reseller_id.id)),
                                                                     ('active','=',True)], context=context)
                if vals:
                    return False
        return True
    
    _inherit = 'crm.lead'
    _name = 'crm.lead'
    _constraints = [
            (_check_reseller,
             'This VAT Number is assigned to a reseller, please create a opportunity without lead',
             ['partner_vat']),
        ]