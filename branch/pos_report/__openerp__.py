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
    "name": "POS Report",
    "version": "0.!",
    "description": """
Manage Reports for the POS Order
================================
Add char print in the local POS touch screen..

Main Features
-------------
* Print on local printers clearly
* Print in character mode (dot printing)
* Open the chashbox and other POS automatizations
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Touchscreen Interface for Shops",
    "depends": ["point_of_sale"],
    "data":[
        "point_of_sale_view.xml",
    ],
    "demo_xml": [ ],
    "js": [
        "static/src/lib/BlobBuilder.js",
        "static/src/lib/FileSaver.js",
        "static/src/js/CubicReport.js",
        "static/src/js/pos_report.js",
    ],
    'qweb' : [
        "static/src/xml/pos_report.xml",
    ],
    "active": False,
    "installable": True,
    "certificate" : "",
}
