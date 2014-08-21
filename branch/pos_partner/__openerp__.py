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
    "name": "POS Order Partner",
    "version": "0.!",
    "description": """
    Manage Partner in POS Order
    ===========================
    Add partner fields (ref and name) on a POS Order, to accomplish legal restrictions of some countries.
    
    Main Features
    -------------
    * Find the ref or VAT number introduced to obtain the name stored on the database
    * Add new partners from POS touch screen
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Touchscreen Interface for Shops",
    "depends": ["point_of_sale"],
    "data":[
    ],
    "demo_xml": [ ],
    "js": [
        "static/src/js/validate.js",
        "static/src/js/pos_partner.js",
    ],
    'qweb' : [
        "static/src/xml/pos_partner.xml",
    ],
    "active": False,
    "installable": True,
    "certificate" : "",
}
