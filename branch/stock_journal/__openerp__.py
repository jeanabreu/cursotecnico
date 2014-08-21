# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
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
    "name": "Stock Journal Extensions",
    "version": "1.0",
    "description": """
Extra Funcionalities on Stock Journal
=====================================

This module adds extra funcionalities on stock journal object, like to sequence, warehouse and carrier relation.

Key Features
------------
* Add sequence on pickings based on stock journal
* Add warehouse on stock journal
* Add carrier default selection by stock journal
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Warehouse",
    "depends": ["stock",
	],
    "data":[
	    "stock_view.xml",
	],
    "demo_xml": [],
    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
