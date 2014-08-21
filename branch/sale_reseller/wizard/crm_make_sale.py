# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
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

class crm_make_sale(osv.osv_memory):
    
    def _selectPartner(self, cr, uid, context=None):
        """
        This function gets default value for partner_id field.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        @return: default value of partner_id field.
        """
        if context is None:
            context = {}

        lead_obj = self.pool.get('crm.lead')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False

        lead = lead_obj.read(cr, uid, active_id, ['partner_id','reseller_id'])
        return lead['reseller_id']

    def _selectCustomer(self, cr, uid, context=None):
        """
        This function gets default value for partner_id field.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        @return: default value of partner_id field.
        """
        if context is None:
            context = {}

        lead_obj = self.pool.get('crm.lead')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False

        lead = lead_obj.read(cr, uid, active_id, ['partner_id','reseller_id'])
        return lead['partner_id']
        
    def _selectReseller(self, cr, uid, context=None):
        """
        This function gets default value for partner_id field.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        @return: default value of partner_id field.
        """
        if context is None:
            context = {}

        lead_obj = self.pool.get('crm.lead')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False

        lead = lead_obj.browse(cr, uid, active_id, context=context)
        return lead.partner_id.reseller
    
    _inherit = "crm.make.sale"
    
    _columns = {
            'reseller_customer_id': fields.many2one('res.partner', string="Reseller's Customer", 
                                                    domain=[('reseller','=',False),('customer','=',True)]),
            'partner_id': fields.many2one('res.partner', 'Reseller / Customer', required=True, 
                                          domain=[('customer','=',True)]),
            'reseller': fields.related('partner_id', 'reseller', type='boolean', string="Reseller"),
        }
    _defaults = {
            'partner_id': _selectPartner,
            'reseller_customer_id': _selectCustomer,
            'reseller': _selectReseller,
        }
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        res = {'value': {}}
        if not partner_id:
            return res
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        res['value']['reseller'] = partner.reseller
        return res
    
    def makeOrder(self, cr, uid, ids, context=None):
        """
        This function  create Quotation on given case.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of crm make sales' ids
        @param context: A standard dictionary for contextual values
        @return: Dictionary value of created sales order.
        """
        sale_obj = self.pool.get('sale.order')
        res = super(crm_make_sale, self).makeOrder(cr, uid, ids, context=context)
        make = self.browse(cr, uid, ids[0], context=context)
        if make.reseller:
            sale_id = res.get('res_id',False)
            if sale_id:
                sale = sale_obj.browse(cr, uid, sale_id, context=context)
                if make.reseller_customer_id:
                    sale_obj.write(cr, uid, [sale.id], {'reseller_customer_id': make.reseller_customer_id.id})
        return res