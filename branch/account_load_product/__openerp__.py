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
    "name": "Initial Product Account Load",
    "version": "1.0",
    "description": """
Manage the Initital Product Account Load
========================================

Used to manage the initial product account load in easy and quickly way.

Key Features
------------
* Create new views to initial product account load
* Integrated with the accounting and products
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Financial",
    "depends": [
        "account_load",
        ],
    "data":[
        "account_load_view.xml",
	    ],
    "demo_xml": [],
    "active": False,
    "installable": True,
    "certificate" : "",
}