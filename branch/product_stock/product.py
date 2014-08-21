# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2014 Cubic ERP - Teradata SAC. (http://cubicerp.com).
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

from osv import fields, osv

class product_product(osv.osv):
    _inherit = 'product.product'
    _name = 'product.product'
    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []
        def _name_get(d):
            name = d.get('name','')
            code = d.get('default_code',False)
            if code:
                name = '[%s] %s' % (code,name)
            if d.get('variants'):
                name = name + ' - %s' % (d['variants'],)
            if d.has_key('qty_available') or d.has_key('virtual_available'):
                name = name + ' (R:%s/V:%s%s%s%s)'%(d.get('qty_available'),d.get('virtual_available'),d.get('loc_rack') and (' '+d.get('loc_rack')) or '',d.get('loc_row') or '',d.get('loc_case') or '')
            return (d['id'], name)

        partner_id = context.get('partner_id', False)

        result = []
        for product in self.browse(cr, user, ids, context=context):
            sellers = filter(lambda x: x.name.id == partner_id, product.seller_ids)
            
            mydict = {'id': product.id, 
                      'variants': product.variants,
                      }
            if product.type <> 'service' and (context.get('product_stock_show',False) or context.has_key('shop')):
                mydict.update({'qty_available': product.qty_available,
                          'virtual_available': product.virtual_available,
                          'loc_rack': product.loc_rack,
                          'loc_row': product.loc_row,
                          'loc_case': product.loc_case,
                          })
            if sellers:
                for s in sellers:
                    mydict['name'] = s.product_name or product.name
                    mydict['default_code'] = s.product_code or product.default_code
            else:
                mydict['name'] = product.name
                mydict['default_code'] = product.default_code
            result.append(_name_get(mydict))
        return result