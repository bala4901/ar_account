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
from lxml import etree
from tools.translate import _

class account_voucher(osv.osv):
	_name = 'account.voucher'
	_inherit = 'account.voucher'
	_order = 'number'
	
	def default_journal_id(self, cr, uid, context={}):
		return False

	def default_voucher_type_id(self, cr, uid, context=None):
		obj_account_voucher_type = self.pool.get('account.voucher_type')
		voucher_type = []

		if context.get('voucher_type', False):
			kriteria = [('name', '=', context['voucher_type'])]

			voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)
			if voucher_type_ids : voucher_type = voucher_type_ids[0]

		return voucher_type

	def default_type(self, cr, uid, context=None):
		obj_account_voucher_type = self.pool.get('account.voucher_type')

		voucher_type_id = self.default_voucher_type_id(cr, uid, context)

		if not voucher_type_id : return False

		voucher_type = obj_account_voucher_type.browse(cr, uid, [voucher_type_id])[0]

		return voucher_type.default_header_type

	def get_amount_to_text(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		amount_to_text = []
		obj_account_voucher = self.pool.get('account.voucher')
		obj_res_currency = self.pool.get('res.currency')

		for account_voucher in obj_account_voucher.browse(cr, uid, ids):
			#amount_to_text = obj_res_currency.terbilang(cr, uid, account_voucher.payment_rate_currency_id.id, account_voucher.amount) # INI CONTOH TERBILANG NYA
			res[account_voucher.id] = '-' #amount_to_text
		return res

	_columns =	{
                                'voucher_type_id' : fields.many2one(obj='account.voucher_type', string='Voucher Type', readonly=True, states={'draft':[('readonly',False)]}),
                                'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')], readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_number' : fields.char(string='Cheque Number', size=50, readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_date' : fields.date(string='Cheque Date', readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account', readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=True, readonly=True),
                                'cheque_recepient' : fields.char(string='Cheque Recepient', size=100, readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_is_giro' : fields.boolean('Is Giro?'),
                                'amount_to_text' : fields.function(fnct=get_amount_to_text, string='Terbilang', type='text', method=True, store=True),
                                'account_id':fields.many2one('account.account', 'Account', required=False, readonly=True, states={'draft':[('readonly',False)]}),
                                
			            }

	_defaults =	{
			            'voucher_type_id' : default_voucher_type_id,
			            'type' : default_type,
			            'journal_id' : default_journal_id,
			            }
			            
        def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
                res = super(account_voucher, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
                x = []
                mod_obj = self.pool.get('ir.model.data')
                obj_account_voucher_type = self.pool.get('account.voucher_type')
                if context is None: context = {}
                
                voucher_type = context.get('voucher_type')

                if voucher_type and view_type == 'form':

                        kriteria = [('name','=',voucher_type)]
                        voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)[0]

                        voucher = obj_account_voucher_type.browse(cr, uid, voucher_type_ids, context=context)

                        result = mod_obj.get_object_reference(cr, uid, voucher.modul_origin, voucher.model_view_form)
                        result = result and result[1] or False
                        view_id = result
                        
                        if voucher.allowed_journal_ids:
                                for journal in voucher.allowed_journal_ids:
                                        x.append(journal.id)
                        domain_journal = list(set(x))

                        for field in res['fields']:
                            if field == 'journal_id':
                                res['fields'][field]['domain'] = [('id','in',domain_journal)]
                return res
			            
	def first_move_line_get(self, cr, uid, voucher_id, move_id, company_currency, current_currency, context=None):
		'''
		Override untuk menyesuaikan field yang berkaitan dengan cek/giro
		'''
		voucher = self.browse(cr, uid, [voucher_id])[0]

		res =	{
					'payment_method' : voucher.payment_method,
					'cheque_number' : voucher.cheque_number,
					'cheque_date' : voucher.cheque_date,
					'cheque_partner_bank_id' : voucher.cheque_partner_bank_id.id,
					'cheque_recepient' : voucher.cheque_recepient
					}

		move_line = super(account_voucher, self).first_move_line_get(cr, uid, voucher_id, move_id, company_currency, current_currency)

		move_line.update(res)

		return move_line
		
	def check_total_voucher(self, cr, uid, id):
		"""
		Method untuk melakukan pengecekan agar total voucher == sum amount semua voucher line
		"""
		
		voucher = self.browse(cr, uid, [id])[0]
		
		total = 0.0
		if voucher.line_ids:
			for line in voucher.line_ids:
				total += line.amount
				
		if voucher.amount == total:
			return True
		else:
			return False
			
	def proforma_voucher(self, cr, uid, ids, context=None):
		"""
		Override
		"""
		
		for id in ids:
			if not self.check_total_voucher(cr, uid, id):
				raise osv.except_osv('Warning!', 'Total voucher is not equal with line total')
				return False

		return super(account_voucher, self).proforma_voucher(cr, uid, ids, context)
		
	def onchange_journal_id(self, cr, uid, ids, journal_id):
		value = {}
		domain = {}
		warning = {}
		
		obj_journal = self.pool.get('account.journal')
				
		if journal_id:
			journal = obj_journal.browse(cr, uid, [journal_id])[0]
			value['account_id'] = journal.default_debit_account_id.id
		
		
		return {'value' : value, 'domain' : domain, 'warning' : warning}
		
	def writeoff_move_line_get(self, cr, uid, voucher_id, line_total, move_id, name, company_currency, current_currency, context=None):
		return False
		
	def action_move_line_create(self, cr, uid, ids, context=None):
		'''
		Confirm the vouchers given in ids and create the journal entries for each of them
		'''
		if context is None:
			context = {}
		move_pool = self.pool.get('account.move')
		move_line_pool = self.pool.get('account.move.line')
		for voucher in self.browse(cr, uid, ids, context=context):
			if voucher.move_id:
				continue
				
			line_total = 0.0

			company_currency = self._get_company_currency(cr, uid, voucher.id, context)
			current_currency = self._get_current_currency(cr, uid, voucher.id, context)
			# we select the context to use accordingly if it's a multicurrency case or not
			context = self._sel_context(cr, uid, voucher.id, context)
			# But for the operations made by _convert_amount, we always need to give the date in the context
			ctx = context.copy()
			ctx.update({'date': voucher.date})
			# Create the account move record.
			move_id = move_pool.create(cr, uid, self.account_move_get(cr, uid, voucher.id, context=context), context=context)
			# Get the name of the account_move just created
			name = move_pool.browse(cr, uid, move_id, context=context).name
		
			# Create the first line of the voucher
			# override untuk mengatasi voucher yang tidak ada header
			if voucher.account_id:
				move_line_id = move_line_pool.create(cr, uid, self.first_move_line_get(cr,uid,voucher.id, move_id, company_currency, current_currency, context), context)
				move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
				line_total = move_line_brw.debit - move_line_brw.credit
		
			rec_list_ids = []
			if voucher.type == 'sale':
				line_total = line_total - self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
			elif voucher.type == 'purchase':
				line_total = line_total + self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
			# Create one move line per voucher line where amount is not 0.0
			line_total, rec_list_ids = self.voucher_move_line_create(cr, uid, voucher.id, line_total, move_id, company_currency, current_currency, context)

			# Create the writeoff line if needed
			ml_writeoff = self.writeoff_move_line_get(cr, uid, voucher.id, line_total, move_id, name, company_currency, current_currency, context)
			if ml_writeoff:
				move_line_pool.create(cr, uid, ml_writeoff, context)
			# We post the voucher.
			self.write(cr, uid, [voucher.id], {
				'move_id': move_id,
				'state': 'posted',
				'number': name,
			})
			if voucher.journal_id.entry_posted:
				move_pool.post(cr, uid, [move_id], context={})
			# We automatically reconcile the account move lines.
			for rec_ids in rec_list_ids:
				if len(rec_ids) >= 2:
				    move_line_pool.reconcile_partial(cr, uid, rec_ids, writeoff_acc_id=voucher.writeoff_acc_id.id, writeoff_period_id=voucher.period_id.id, writeoff_journal_id=voucher.journal_id.id)
		return True		
		
		
        
        
							
account_voucher()							
	
