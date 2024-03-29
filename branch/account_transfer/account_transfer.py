# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#     Copyright (C) 2012 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
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
from openerp.tools.translate import _
from decimal import Decimal
import openerp.addons.decimal_precision as dp
import time

class account_transfer(osv.osv):

    def _get_balance(self, src_journal, dst_journal, company):
        src_balance = dst_balance = 0.0
        #import pdb; pdb.set_trace()
        if src_journal.default_credit_account_id.id == src_journal.default_debit_account_id.id:
            if not src_journal.currency or company.currency_id.id == src_journal.currency.id:
                src_balance = src_journal.default_credit_account_id.balance
            else:
                src_balance = src_journal.default_credit_account_id.foreign_balance
        else:
            if not src_journal.currency or company.currency_id.id == src_journal.currency.id:
                src_balance = src_journal.default_debit_account_id.balance - src_journal.default_credit_account_id.balance
            else:
                src_balance = src_journal.default_debit_account_id.foreign_balance - src_journal.default_credit_account_id.foreign_balance
        if dst_journal.default_credit_account_id.id == dst_journal.default_debit_account_id.id:
            if not dst_journal.currency or company.currency_id.id == dst_journal.currency.id:
                dst_balance = dst_journal.default_credit_account_id.balance
            else:
                dst_balance = dst_journal.default_credit_account_id.foreign_balance
        else:
            if not dst_journal.currency or company.currency_id.id == dst_journal.currency.id:
                dst_balance = dst_journal.default_debit_account_id.balance - dst_journal.default_credit_account_id.balance
            else:
                dst_balance = dst_journal.default_debit_account_id.foreign_balance - dst_journal.default_credit_account_id.foreign_balance
        
        return (src_balance, dst_balance)

    def _balance(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for trans in self.browse(cr, uid, ids, context=context):
            src_balance, dst_balance = self._get_balance(trans.src_journal_id,trans.dst_journal_id,trans.company_id)
            exchange = False
            if trans.dst_journal_id.currency.id != trans.src_journal_id.currency.id:
                exchange = True
            res[trans.id] = {
                    'src_balance':src_balance,
                    'dst_balance':dst_balance,
                    'exchange':exchange,
                    'exchange_inv': (trans.exchange_rate and 1.0 / trans.exchange_rate or 0.0)
                }
        return res

    def _get_type (self, cr, uid, context=None):
        return [('transfer','Transfer')]

    STATE_SELECTION = [
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done'),
        ('cancel','Cancel'),
    ]

    _columns = {
            'company_id' : fields.many2one('res.company','Company', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'type': fields.selection(_get_type,'Type', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'name': fields.char('Number', size=32, required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'date': fields.date('Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'period_id': fields.many2one('account.period','Period', readonly=True, states={'draft':[('readonly',False)]}),
            'origin': fields.char('Origin', size=128, readonly=True, states={'draft':[('readonly',False)]},help="Origin Document"),
            'account_analytic_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True, states={'draft':[('readonly',False)]}),
            'voucher_ids': fields.one2many('account.voucher','transfer_id', string='Payments', readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}),
            'src_journal_id': fields.many2one('account.journal','Source Journal',required=True, domain=[('type','in',['cash','bank'])], select=True, readonly=True, states={'draft':[('readonly',False)]}),
            'src_partner_id': fields.many2one('res.partner','Source Partner', select=True),
            'src_balance': fields.function(_balance, digits_compute=dp.get_precision('Account'), string='Current Source Balance', type='float', readonly=True, multi='balance', help="Include all account moves in draft and confirmed state"),
            'src_amount': fields.float('Source Amount',required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'src_have_partner': fields.related('src_journal_id','have_partner',type='boolean',string='Have Partner',readonly=True),
            'dst_journal_id': fields.many2one('account.journal','Destinity Journal',required=True, domain=[('type','in',['cash','bank'])], select=True, readonly=True, states={'draft':[('readonly',False)]}),
            'dst_partner_id': fields.many2one('res.partner','Destinity Partner', select=True),
            'dst_balance': fields.function(_balance, digits_compute=dp.get_precision('Account'), string='Current Destinity Balance', type='float', readonly=True, multi='balance', help="Include all account moves in draft and confirmed state"),
            'dst_amount': fields.float('Destinity Amount',required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'dst_have_partner': fields.related('dst_journal_id','have_partner',type='boolean',string='Have Partner',readonly=True),
            'exchange_rate': fields.float('Exchange Rate', digits_compute=dp.get_precision('Exchange'), readonly=True, states={'draft':[('readonly',False)]}),
            'exchange': fields.function(_balance, string='Have Exchange', type='boolean', readonly=True, multi='balance'),
            'exchange_inv': fields.function(_balance, string='1 / Exchange Rate', type='float', digits_compute=dp.get_precision('Exchange'), readonly=True, multi='balance'),
            'adjust_move': fields.many2one('account.move','Adjust Move', readonly=True, help="Adjust move usually by difference in the money exchange"),
            'state': fields.selection(STATE_SELECTION,string='State',track_visibility='onchange',readonly=True),
        }
    _defaults = {
            'type': 'transfer',
            'name': lambda s,cr,u,c: s.pool.get('ir.sequence').get(cr, u, 'account.transfer'),
            'company_id': lambda s,cr,u,c: s.pool.get('res.users').browse(cr,u,u).company_id.id,
            'date': lambda *a: time.strftime('%Y-%m-%d'),
            'exchange_rate': 1.0,
            'exchange_inv': 1.0,
            'state': 'draft',
        }
    _sql_constraints = [('name_unique','unique(company_id,name)',_('The number must be unique!'))]
    _name = 'account.transfer'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Account Cash and Bank Transfer'
    _order = 'name desc'

    def voucher_get(self, cr, uid, trans, context=None):
        res = {}
        res['transfer_id'] = trans.id
        res['type'] = 'transfer'
        res['company_id'] = trans.company_id.id
        res['reference'] = trans.name.encode('utf-8') + str(trans.origin and (' - ' + trans.origin.encode('utf-8')) or '')
        res['line_ids'] = [(0,0,{})]
        res['line_ids'][0][2]['account_analytic_id'] = trans.account_analytic_id and trans.account_analytic_id.id or 0
        res['line_ids'][0][2]['name'] = trans.origin
        return res

    def unlink(self, cr, uid, ids, context=None):
        for trans in self.browse(cr, uid, ids, context=context):
            if trans.state not in ('draft'):
                raise osv.except_osv(_('User Error!'),_('You cannot delete a not draft transfer "%s"') % trans.name)
        return super(account_transfer, self).unlink(cr, uid, ids, context=context)

    def copy(self, cr, uid, id, defaults, context=None):
        defaults['name'] = self.pool.get('ir.sequence').get(cr, uid, 'account.transfer')
        defaults['voucher_ids'] = []
        return super(account_transfer, self).copy(cr, uid, id, defaults, context=context)

    def onchange_amount(self, cr, uid, ids, field, src_amount, dst_amount, exchange_rate, context=None):
        res = {'value':{}}
        new_src = 0
        new_dst = 0
        new_ext_inv = exchange_rate and 1.0 / exchange_rate or 0.0
        if field == 'src_amount':
            new_src = src_amount
            new_dst = src_amount * exchange_rate
        elif field == 'dst_amount':
            new_src = exchange_rate and dst_amount / exchange_rate or 0.0
            new_dst = dst_amount
        elif field == 'exchange_rate':
            new_src = src_amount
            new_dst = src_amount * exchange_rate
        if round(new_src, abs(Decimal(str(src_amount)).as_tuple().exponent)) != src_amount:
            res['value']['src_amount'] = new_src
        if round(new_dst, abs(Decimal(str(dst_amount)).as_tuple().exponent)) != dst_amount:
            res['value']['dst_amount'] = new_dst
        res['value']['exchange_inv'] = new_ext_inv
        return res
        
    def onchange_journal(self, cr, uid, ids, src_journal_id, dst_journal_id, date, exchange_rate, src_amount):
        res = {'value':{}}
        if not(src_journal_id and dst_journal_id):
            return res
        src_journal = self.pool.get('account.journal').browse(cr, uid, src_journal_id)
        dst_journal = self.pool.get('account.journal').browse(cr, uid, dst_journal_id)
        res['value']['src_balance'], res['value']['dst_balance'] = self._get_balance(src_journal,dst_journal,src_journal.company_id)
        res['value']['exchange'] = (src_journal.currency.id != dst_journal.currency.id)
        res['value']['src_have_partner'], res['value']['dst_have_partner'] = src_journal.have_partner, dst_journal.have_partner
        res['value']['exchange_rate'] = exchange_rate
        if res['value']['exchange']:
            res['value']['exchange_rate'] = (src_journal.currency and src_journal.currency.rate or src_journal.company_id.currency_id.rate) and ((dst_journal.currency and dst_journal.currency.rate or dst_journal.company_id.currency_id.rate) / (src_journal.currency and src_journal.currency.rate or src_journal.company_id.currency_id.rate)) or 0.0
        else:
            res['value']['exchange_rate'] = 1.0
        res['value']['exchange_inv'] = res['value']['exchange_rate'] and (1.0 / res['value']['exchange_rate']) or 0.0
        res['value']['dst_amount'] = res['value']['exchange_rate'] * src_amount
        return res

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        for trans in self.browse(cr, uid, ids, context=context):
            context['company_id'] = trans.company_id.id
            sval = self.voucher_get(cr, uid, trans, context=context)
            dval = self.voucher_get(cr, uid, trans, context=context)
            sval['company_id'] = trans.company_id.id
            dval['company_id'] = trans.company_id.id
            sval['journal_id'] = trans.src_journal_id.id
            dval['journal_id'] = trans.dst_journal_id.id
            if trans.period_id:
                sval['period_id'] = trans.period_id.id
                dval['period_id'] = trans.period_id.id
            sval['date'] = trans.date
            dval['date'] = trans.date
            sval['account_id'] = trans.src_journal_id.default_credit_account_id.id
            dval['account_id'] = trans.dst_journal_id.default_debit_account_id.id
            sval['payment_rate'] = trans.src_journal_id.currency.id and trans.company_id.currency_id.id <> trans.src_journal_id.currency.id and trans.exchange_rate or 1.0
            dval['payment_rate'] = trans.dst_journal_id.currency.id and trans.company_id.currency_id.id <> trans.dst_journal_id.currency.id  and trans.exchange_inv or 1.0
            sval['payment_rate_currency_id'] = trans.dst_journal_id.currency.id or trans.company_id.currency_id.id
            dval['payment_rate_currency_id'] = trans.src_journal_id.currency.id or trans.company_id.currency_id.id
            sval['line_ids'][0][2]['amount'] = sval['amount'] = trans.src_amount
            dval['line_ids'][0][2]['amount'] = dval['amount'] = trans.dst_amount
            sval['line_ids'][0][2]['type'] = 'dr'
            dval['line_ids'][0][2]['type'] = 'cr'
            sval['line_ids'][0][2]['account_id'] = trans.dst_journal_id.default_debit_account_id.id
            if trans.src_partner_id.id ^ trans.dst_partner_id.id:
                sval['partner_id'] = trans.src_have_partner and trans.src_partner_id.id or trans.dst_partner_id.id
            else:
                sval['partner_id'] = trans.src_have_partner and trans.src_partner_id.id or trans.company_id.partner_id.id
                dval['partner_id'] = trans.dst_have_partner and trans.dst_partner_id.id or trans.company_id.partner_id.id
                sval['line_ids'][0][2]['account_id'] = dval['line_ids'][0][2]['account_id'] = trans.src_journal_id.account_transit.id
                voucher_obj.create(cr, uid, dval, context=context)
            voucher_obj.create(cr, uid, sval, context=context)
        return self.write(cr, uid, ids, {'state':'confirm'},context=context)

    def action_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        move_obj = self.pool.get('account.move')
        for trans in self.browse(cr, uid, ids, context=context):
            paid_amount = []
            for voucher in trans.voucher_ids:
                (voucher.state == 'draft') and voucher_obj.proforma_voucher(cr, uid, [voucher.id], context=context)
                sign = (voucher.journal_id.id == trans.src_journal_id.id) and 1 or -1
                paid_amount.append(sign * voucher_obj._paid_amount_in_company_currency(cr, uid, [voucher.id], '', '')[voucher.id])
                #paid_amount.append(sign * voucher.paid_amount_in_company_currency)
            sum_amount = sum(paid_amount)
            if len(paid_amount) > 1 and sum_amount != 0.0:
                context['company_id'] = trans.company_id.id
                periods = self.pool.get('account.period').find(cr, uid, context=context)
                period_id = trans.period_id.id or (periods and periods[0] or False)
                move = {}
                move['journal_id'] = trans.dst_journal_id.id
                move['company_id'] = trans.company_id.id
                move['period_id'] = period_id
                move['ref'] = trans.name + str(trans.origin and (' - ' + trans.origin) or '')
                move['date'] = trans.date
                move['line_id'] = [(0,0,{}),(0,0,{})]
                move['line_id'][0][2]['name'] = trans.name
                move['line_id'][1][2]['name'] = trans.name
                if sum_amount > 0:
                    move['line_id'][0][2]['account_id'] = trans.dst_journal_id.default_debit_account_id.id
                    move['line_id'][1][2]['account_id'] = trans.src_journal_id.account_transit.id #trans.company_id.income_currency_exchange_account_id.id
                    move['line_id'][0][2]['debit'] = sum_amount
                    move['line_id'][1][2]['credit'] = sum_amount
                else:
                    move['line_id'][0][2]['account_id'] = trans.dst_journal_id.default_credit_account_id.id
                    move['line_id'][1][2]['account_id'] = trans.src_journal_id.account_transit.id #trans.company_id.expense_currency_exchange_account_id.id
                    move['line_id'][1][2]['debit'] = -1 * sum_amount
                    move['line_id'][0][2]['credit'] = -1 * sum_amount
                move_id = move_obj.create(cr, uid, move, context=context)
                self.write(cr, uid, [trans.id], {'adjust_move':move_id}, context=context)
        return self.write(cr, uid, ids, {'state':'done'},context=context)

    def action_cancel(self, cr, uid, ids, context=None):
        voucher_obj = self.pool.get('account.voucher')
        move_obj = self.pool.get('account.move')
        #import pdb; pdb.set_trace()
        for trans in self.browse(cr, uid, ids, context=context):
            for voucher in trans.voucher_ids:
                voucher_obj.unlink(cr, uid, [voucher.id], context=context)
            trans.adjust_move and move_obj.unlink(cr, uid, [trans.adjust_move.id], context=context)
        return self.write(cr, uid, ids, {'state':'cancel'},context=context)

    def action_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'})
#        wf_service = netsvc.LocalService("workflow")
#        for trans_id in ids:
#            wf_service.trg_delete(uid, 'account.transfer', trans_id, cr)
#            wf_service.trg_create(uid, 'account.transfer', trans_id, cr)
        return True

account_transfer()