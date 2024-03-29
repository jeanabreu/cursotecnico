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
{
    "name": "Sale Reseller",
    "version": "1.0",
    "author": "Cubic ERP",
    "category": "sales",
    "description": """
    Add reseller funcionality on sales (partner, sale order and oportunities)
    """,
    "depends": [
            "base_status",
            "sale",
            "sale_crm",
        ],
    "demo_xml": [
        ],
    "data": [
	       "partner_view.xml",
           "crm_view.xml",
           "sale_view.xml",
           "wizard/crm_make_sale_view.xml",
        ],
    "active": False,
    "installable": True
}