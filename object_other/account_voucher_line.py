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
from datetime import datetime

class account_voucher_line(osv.osv):
	_name = 'account.voucher.line'
	_inherit = 'account.voucher.line'

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
		
		#ine.reconcile_partial_id and line.amount_residual_currency < 0:
		    # skip line that are totally used within partial reconcile
		    #pass
		if line.currency_id and currency_id==line.currency_id.id:
		    amount_original = abs(line.amount_currency)
		    amount_unreconciled = abs(line.amount_residual_currency)
		else:
		    amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0)
		    amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual))
		line_currency_id = line.currency_id and line.currency_id.id or company_currency
		rs = {
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
			
		return {'value' : value, 'domain' : domain, 'warning' : warning}		

							
account_voucher_line()							
	
