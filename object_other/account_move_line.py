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

class account_move_line(osv.osv):
	_name = 'account.move.line'
	_inherit = 'account.move.line'
	
	def _amount_residual(self, cr, uid, ids, field_names, args, context=None):
		"""
		   This function returns the residual amount on a receivable or payable account.move.line.
		   By default, it returns an amount in the currency of this journal entry (maybe different
		   of the company currency), but if you pass 'residual_in_company_currency' = True in the
		   context then the returned amount will be in company currency.
		"""
		res = {}
		if context is None:
		    context = {}
		cur_obj = self.pool.get('res.currency')
		for move_line in self.browse(cr, uid, ids, context=context):
		    res[move_line.id] = {
		        'amount_residual': 0.0,
		        'amount_residual_currency': 0.0,
		    }

		    if move_line.reconcile_id:
		        continue
		    if not move_line.account_id.reconcile:
		        #this function does not suport to be used on move lines not related to payable or receivable accounts
		        continue

		    if move_line.currency_id:
		        move_line_total = move_line.amount_currency
		        sign = move_line.amount_currency < 0 and -1 or 1
		    else:
		        move_line_total = move_line.debit - move_line.credit
		        sign = (move_line.debit - move_line.credit) < 0 and -1 or 1
		    line_total_in_company_currency =  move_line.debit - move_line.credit
		    context_unreconciled = context.copy()
		    if move_line.reconcile_partial_id:
		        for payment_line in move_line.reconcile_partial_id.line_partial_ids:
		            if payment_line.id == move_line.id:
		                continue
		            if payment_line.currency_id and move_line.currency_id and payment_line.currency_id.id == move_line.currency_id.id:
		                    move_line_total += payment_line.amount_currency
		            else:
		                if move_line.currency_id:
		                    context_unreconciled.update({'date': payment_line.date})
		                    amount_in_foreign_currency = cur_obj.compute(cr, uid, move_line.company_id.currency_id.id, move_line.currency_id.id, (payment_line.debit - payment_line.credit), round=False, context=context_unreconciled)
		                    move_line_total += amount_in_foreign_currency
		                else:
		                    move_line_total += (payment_line.debit - payment_line.credit)
		            line_total_in_company_currency += (payment_line.debit - payment_line.credit)

		    result = move_line_total
		    res[move_line.id]['amount_residual_currency'] =  sign * (move_line.currency_id and self.pool.get('res.currency').round(cr, uid, move_line.currency_id, result) or result)
		    res[move_line.id]['amount_residual'] = sign * line_total_in_company_currency
		return res	
	
	_columns =	{
						'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')]),
                        'cheque_number' : fields.char(string='Cheque Number', size=50),
                        'cheque_date' : fields.date(string='Cheque Date'),
                        'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account'),
                        'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=True, readonly=True),
                        'cheque_recepient' : fields.char(string='Cheque Recepient', size=100),
                        'cheque_is_giro' : fields.boolean('Is Giro?'),
						'amount_residual_currency': fields.function(_amount_residual, string='Residual Amount', multi="residual", help="The residual amount on a receivable or payable of a journal entry expressed in its currency (maybe different of the company currency)."),
						'amount_residual': fields.function(_amount_residual, string='Residual Amount', multi="residual", help="The residual amount on a receivable or payable of a journal entry expressed in the company currency."),                        
                        }

	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_move_line, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_move_line, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_move_line, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')

account_move_line()




