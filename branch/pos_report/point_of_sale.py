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

class pos_config(osv.osv):
    _name = "pos.config"
    _inherit = "pos.config"

    _columns = {
        'javascript_report': fields.boolean('JavaScript Report', help="Mark this option to customize your local printing using a character printer"),
        'javascript_report_src': fields.text('JavaScript Report'),
    }
    _defaults = {
        'javascript_report_src': """
            txt = ESC + '@' + BEL;
            txt += this.company.name + CR;
            txt += this.company.rml_header1 + CR;
            txt += this.shop_obj.name + CR;
            txt += 'R.U.C.:' + String(this.company.vat).substr(2) + ' Serie:' + this.shop_obj.printer_serial + CR;
            txt += CR;
            for(i in order){
                txt += pad(order[i].get('name'),28) + 
                        ' ' + pad(order[i].get('quantity').toFixed(0),-3) +
                        ' ' + pad((order[i].get('list_price') * (1 - order[i].get('discount')/100) * order[i].get('quantity') * iva_percent).toFixed(2),-8) + CR;
            }
            txt += CR;
            txt += 'Total: ' + pos.get('currency').symbol + ' ' + this.currentOrder.getTotal().toFixed(2) + CR;
            txt += CR;
            for(i in pline){
                if(pline[i].getAmount() < 0) continue;
                txt += pline[i].get('journal_id')[1] + 
                        ' ' + pos.get('currency').symbol + ' ' + (pline[i].getAmount()).toFixed(2) + CR;
            }
            txt += CR;
            for(i in pline){
                if(pline[i].getAmount() >= 0) continue;
                txt += 'Vuelto: ' + pos.get('currency').symbol + ' ' + (pline[i].getAmount() * -1).toFixed(2) + CR;
            }
            txt += CR;
            txt += this.company.rml_footer1 + CR;
            txt += now.toString(Date.CultureInfo.formatPatterns.shortDate + ' ' + 
                    Date.CultureInfo.formatPatterns.longTime) +
                    ' ' + this.user.login + CR;
            txt += this.currentOrder.getName() + CR;
        """,
    }