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
    "name": "Account Invoice Swap",
    "version": "1.0",
    "description": """
Manage the Exchange of Invoices
===============================

This module manage the exchange or swap of supplier invoices with customer invoices, allowing the reconciliation of differents accounts.

Key Features
------------
* Add a check on partner form to allow the invoice swap
* Add a field on partner form to show the partial reconcile
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Financial",
    "depends": [
        "account",
        ],
    "data":[
        "partner_view.xml",
	    ],
    "demo_xml": [],
    "active": False,
    "installable": True,
    "certificate" : "",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: