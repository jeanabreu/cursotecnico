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
    
    def _check_unique_vat(self, cr, uid, ids, context=None):
        for lead in self.browse(cr, uid, ids, context=context):
            if lead.partner_vat:
                vals = self.search(cr, uid, [('company_id','=',lead.company_id.id),('partner_vat','=',lead.partner_vat),('state','in',['draft','open','pending']),
                                             ('id','!=',lead.id)], context=context)
                if vals:
                    return False
        return True
    
    def check_vat(self, cr, uid, ids, context=None):
        user_company = self.pool.get('res.users').browse(cr, uid, uid).company_id
        partner_obj = self.pool.get('res.partner')
        if user_company.vat_check_vies:
            # force full VIES online check
            check_func = partner_obj.vies_vat_check
        else:
            # quick and partial off-line checksum validation
            check_func = partner_obj.simple_vat_check
        for lead in self.browse(cr, uid, ids, context=context):
            if not lead.partner_vat:
                continue
            vat_country, vat_number = partner_obj._split_vat(lead.partner_vat)
            if not check_func(cr, uid, vat_country, vat_number, context=context):
                return False
        return True
    
    _inherit = 'crm.lead'
    _name = 'crm.lead'
    _columns = {
        'partner_vat': fields.char('Partner VAT',32),
    }
    _constraints = [
            (check_vat,
             'This VAT number does not seem to be valid',
             ['partner_vat']),
            (_check_unique_vat,
             'There are another lead or oportunity active with the same VAT Number',
             ['partner_vat']),
        ]
    
    def _lead_create_contact_vals(self, cr, uid, lead, name, is_company, parent_id=False, context=None):
        res = super(crm_lead,self)._lead_create_contact_vals(cr, uid, lead, name, is_company, parent_id=parent_id, context=context)
        if is_company:
            res['vat'] = lead.partner_vat
            res['ref'] = lead.partner_vat[2:]
        return res
    
    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        res = super(crm_lead,self).onchange_partner_id(cr, uid, ids, part, email=email)
        res['value']['partner_vat'] = self.pool.get('res.partner').browse(cr, uid, part).vat
        return res
    
    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        res = super(crm_lead,self).on_change_partner(cr, uid, ids, partner_id, context=context)
        res['value']['partner_vat'] = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context).vat
        return res