# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution   
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from osv import fields, osv
import decimal_precision as dp

class account_voucher_line(osv.osv):
    _name = 'account.voucher.line'
    _inherit = 'account.voucher.line'

    def function_amount_all(self, cr, uid, ids, name, args, context={}):
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] =   {
                                'total_dr' : 0.0,
                                'total_cr' : 0.0,
                                }
            if line.type == 'dr':
                res[line.id]['total_dr'] = line.amount
            else:
                res[line.id]['total_cr'] = line.amount
        return res

    def _compute_balance(self, cr, uid, ids, name, args, context=None):
        currency_pool = self.pool.get('res.currency')
        rs_data = {}
        for line in self.browse(cr, uid, ids, context=context):
            ctx = context.copy()
            ctx.update({'date': line.voucher_id.date})
            voucher_rate = self.pool.get('res.currency').read(cr, uid, line.voucher_id.currency_id.id, ['rate'], context=ctx)['rate']
            res = {}
            company_currency = line.voucher_id.journal_id.company_id.currency_id.id
            voucher_currency = line.voucher_id.currency_id and line.voucher_id.currency_id.id or company_currency
            move_line = line.move_line_id or False

            if not move_line:
                res['amount_original'] = 0.0
                res['amount_unreconciled'] = 0.0
            elif move_line.currency_id and voucher_currency==move_line.currency_id.id:
                res['amount_original'] = abs(move_line.amount_currency)
                res['amount_unreconciled'] = abs(move_line.amount_residual_currency)
            else:
                #always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                res['amount_original'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, move_line.credit or move_line.debit or 0.0, context=ctx)
                res['amount_unreconciled'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, abs(move_line.amount_residual), context=ctx)

            rs_data[line.id] = res
        return rs_data

    _columns =   {
                'total_dr' : fields.function(string='Total Debit', fnct=function_amount_all, type='float', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                'total_cr' : fields.function(string='Total Credit', fnct=function_amount_all, type='float', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                'product_id' : fields.many2one(obj='product.product', string='Product', readonly=True, states={'draft':[('readonly',False)]}),
                'partner_id' : fields.many2one(string='Partner', obj='res.partner', ondelete='restrict'),
                'amount_original': fields.function(_compute_balance, multi='dc', type='float', string='Original Amount', store=True, digits_compute=dp.get_precision('Account')),
                'amount_unreconciled': fields.function(_compute_balance, multi='dc', type='float', string='Open Balance', store=True, digits_compute=dp.get_precision('Account')),
                }
                
    def onchange_product_id(self, cr, uid, ids, product_id):

        obj_res_product = self.pool.get('product.product')

        value = {}
        domain = {}
        warning = {}

        if product_id:
            account_id = obj_res_product.browse(cr, uid, product_id).property_account_expense.id
            value.update({'account_id' : account_id})
        
        return {'value' : value, 'domain' : domain, 'warning' : warning}

    

    def default_get(self, cr, uid, fields_list, context=None):
        res = super(account_voucher_line, self).default_get(cr, uid, fields_list, context)

        if context.get('default_detail_type_selection', False):
            res.update({'type' : context.get('default_detail_type_selection', False)})
    
        return res

    def compute_amount(self, cr, uid, move_id, journal_id, currency_id):
        currency_pool = self.pool.get('res.currency')
        obj_move = self.pool.get('account.move.line')
        obj_journal = self.pool.get('account.journal')
        
        rs = {}
        
        line = obj_move.browse(cr, uid, [move_id])[0]
        journal = obj_journal.browse(cr, uid, [journal_id])[0]
        
        currency_id = currency_id or journal.company_id.currency_id.id
        company_currency = journal.company_id.currency_id.id

        context = {'date' : line.date}
        
        if line.currency_id and currency_id==line.currency_id.id:
            amount_original = abs(line.amount_currency)
            amount_unreconciled = abs(line.amount_residual_currency)
        else:
            amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0,context=context)
            amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual),context=context)

        rs =    {
                'amount_original': amount_original,
                'amount': amount_unreconciled,
                'amount_unreconciled': amount_unreconciled,
                }

        return rs
        
    def onchange_move_id(self, cr, uid, ids, move_id, journal_id, currency_id):
        value = {}
        domain = {}
        warning = {}
        
        obj_move = self.pool.get('account.move.line')
                
        if move_id:
            move = obj_move.browse(cr, uid, [move_id])[0]
            value['account_id'] = move.account_id.id
            value['name'] = move.name
            value['date_original'] = move.date
            value['date_due'] = move.date_maturity
            res = self.compute_amount(cr, uid, move_id, journal_id, currency_id)
            value['amount'] = res['amount']
            value['amount_original'] = res['amount_original']
            value['amount_unreconciled'] = res['amount_unreconciled']
            value['partner_id'] = move.partner_id and move.partner_id.id or False
            
        return {'value' : value, 'domain' : domain, 'warning' : warning}        

    def onchange_partner_id(self, cr, uid, ids, move_id):
        value = {}
        domain = {}
        warning = {}

        obj_move = self.pool.get('account.move.line')

        if move_id:
            move = obj_move.browse(cr, uid, [move_id])[0]
            value['partner_id'] = move.partner_id and move.partner_id.id or False

        return {'value' : value, 'domain' : domain, 'warning' : warning}




                            
account_voucher_line()                          
    
