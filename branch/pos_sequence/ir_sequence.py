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

class ir_sequence(osv.osv):
    _name = "ir.sequence"
    _inherit = "ir.sequence"

    def _dict_next(self, cr, uid, seq_ids, context=None):
        if not seq_ids:
            return False
        if context is None:
            context = {}
        force_company = context.get('force_company')
        if not force_company:
            force_company = self.pool.get('res.users').browse(cr, uid, uid).company_id.id
        sequences = self.read(cr, uid, seq_ids, ['name','company_id','implementation','number_next','prefix','suffix','padding','number_increment'])
        preferred_sequences = [s for s in sequences if s['company_id'] and s['company_id'][0] == force_company ]
        seq = preferred_sequences[0] if preferred_sequences else sequences[0]
        if seq['implementation'] == 'standard':
            cr.execute("SELECT nextval('ir_sequence_%03d')" % seq['id'])
            seq['number_next'] = cr.fetchone()
        else:
            cr.execute("SELECT number_next FROM ir_sequence WHERE id=%s FOR UPDATE NOWAIT", (seq['id'],))
            cr.execute("UPDATE ir_sequence SET number_next=number_next+number_increment WHERE id=%s ", (seq['id'],))
        d = self._interpolation_dict()
        try:
            interpolated_prefix = self._interpolate(seq['prefix'], d)
            interpolated_suffix = self._interpolate(seq['suffix'], d)
        except ValueError:
            raise osv.except_osv(_('Warning'), _('Invalid prefix or suffix for sequence \'%s\'') % (seq.get('name')))
        return {'prefix': interpolated_prefix,
                'padding': seq['padding'],
                'number_next': seq['number_next'],
                'suffix': interpolated_suffix,
                'number_increment': seq['number_increment'],
                'next': interpolated_prefix + '%%0%sd' % seq['padding'] % seq['number_next'] + interpolated_suffix,
            } 
     

    def dict_next_by_id(self, cr, uid, sequence_id, context=None):
        """ Draw an interpolated string using the specified sequence."""
        self.check_access_rights(cr, uid, 'read')
        company_ids = self.pool.get('res.company').search(cr, uid, [], context=context) + [False]
        ids = self.search(cr, uid, ['&',('id','=', sequence_id),('company_id','in',company_ids)])
        return self._dict_next(cr, uid, ids, context)
        
    def _dict(self, cr, uid, seq_ids, context=None):
        if not seq_ids:
            return False
        if context is None:
            context = {}
        force_company = context.get('force_company')
        if not force_company:
            force_company = self.pool.get('res.users').browse(cr, uid, uid).company_id.id
        sequences = self.read(cr, uid, seq_ids, ['name','company_id','implementation','number_next','prefix','suffix','padding','number_increment'])
        preferred_sequences = [s for s in sequences if s['company_id'] and s['company_id'][0] == force_company ]
        seq = preferred_sequences[0] if preferred_sequences else sequences[0]
        d = self._interpolation_dict()
        try:
            interpolated_prefix = self._interpolate(seq['prefix'], d)
            interpolated_suffix = self._interpolate(seq['suffix'], d)
        except ValueError:
            raise osv.except_osv(_('Warning'), _('Invalid prefix or suffix for sequence \'%s\'') % (seq.get('name')))
        return {'prefix': interpolated_prefix,
                'padding': seq['padding'],
                'number_next': seq['number_next'],
                'suffix': interpolated_suffix,
                'number_increment': seq['number_increment'],
            }
        
    def dict_by_ids(self, cr, uid, sequence_ids, context=None):
        res = {}
        self.check_access_rights(cr, uid, 'read')
        company_ids = self.pool.get('res.company').search(cr, uid, [], context=context) + [False]
        ids = self.search(cr, uid, ['&',('id','in', sequence_ids),('company_id','in',company_ids)])
        for _id in ids:
            res[_id] = self._dict(cr, uid, [_id], context)
        return res