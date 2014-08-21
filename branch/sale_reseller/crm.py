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

from openerp.addons.base_status import base_stage as bs
from openerp.osv import osv, fields
from openerp.tools.translate import _

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    
    _columns = {
            'reseller_id': fields.many2one('res.partner', string="Reseller", domain=[('reseller','=',True)]),
        }
    
    def _lead_create_contact_vals(self, cr, uid, lead, name, is_company, parent_id=False, context=None):
        res = super(crm_lead,self)._lead_create_contact_vals(cr, uid, lead, name, is_company, parent_id=parent_id, context=context)
        if lead.reseller_id:
            res['reseller_id'] = lead.reseller_id.id
        return res
    
    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        res = super(crm_lead,self).onchange_partner_id(cr, uid, ids, part, email=email)
        res['value']['reseller_id'] = self.pool.get('res.partner').browse(cr, uid, part).reseller_id.id
        return res
    
    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        res = super(crm_lead,self).on_change_partner(cr, uid, ids, partner_id, context=context)
        res['value']['reseller_id'] = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context).reseller_id.id
        return res