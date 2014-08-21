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
    "name": "Stock and Production Serial Number",
    "version": "1.0",
    "description": """
Adds unique serial numbers to the production lots and stock moves

    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Warehouse",
    "depends": ["stock",
                "sale",
	],
    "data":[
	    "stock_view.xml",
	    "product_view.xml",
	    "stock_serial_view.xml",
	    "stock_serial.xml",
	],
    "demo_xml": [],
    "update_xml": [
	],
    "active": False,
    "installable": True,
    "certificate" : "",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
