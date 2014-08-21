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
    "name": "Initial Account Load",
    "version": "1.0",
    "description": """
Manage the Initital Account Load
================================

Used to manage the initial account load in easy and quickly way.

Key Features
------------
* Create new views to initial account load
* Integrated with the accounting
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Financial",
    "depends": [
        "account",
        "analytic",
        ],
    "data":[
#        "account_view.xml",
        "account_load_view.xml",
        "security/account_load_security.xml",
        "security/ir.model.access.csv",
	    ],
    "demo_xml": [],
    "active": False,
    "installable": True,
    "certificate" : "",
}