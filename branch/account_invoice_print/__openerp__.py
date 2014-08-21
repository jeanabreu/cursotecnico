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
    "name": "Account Invoice Print",
    "version": "1.0",
    "description": """
Manage the Printing on Invoices
===============================

The invoices usually requiere a different printed format based on the asocied journal. 
This module allow to you to associate a report to a journal in order to print the correct report in the invoice print button. 

Key Features
------------
* Add report field on the journals
* Add funcionality on invoice print button
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Financial",
    "depends": [
        "account",
        ],
    "data":[
        "account_view.xml",
	    ],
    "demo_xml": [],
    "active": False,
    "installable": True,
    "certificate" : "",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: