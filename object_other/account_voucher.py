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
import netsvc

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
			amount_to_text = obj_res_currency.terbilang(cr, uid, account_voucher.payment_rate_currency_id.id, account_voucher.amount) # INI CONTOH TERBILANG NYA
			res[account_voucher.id] = amount_to_text
		return res
		
	def default_payment_option(self, cr, uid, context={}):
		return 'with_writeoff'

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
                                'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('waiting','Waiting For Approval'),('ready','Ready To Process'),('proforma','Pro-forma'),('posted','Posted'),('cancel','Cancelled')], string='State', readonly=True),
                                
			            }

	_defaults =	{
			            'voucher_type_id' : default_voucher_type_id,
			            'type' : default_type,
			            'journal_id' : default_journal_id,
			            'payment_option' : default_payment_option,
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
		
	def workflow_action_confirm(self, cr, uid, ids, context={}):
		"""
		Method yang dijalankan ketika confirm
		
		* Merubah state
		"""
		for id in ids:
				
			self.write(cr, uid, [id], {'state':'confirm'})
		return True
	
	def workflow_action_waiting(self, cr, uid, ids, context={}):
		"""
		Method yang dijalankan ketika waiting
		
		* Merubah state
		"""	
		for id in ids:
			#TODO:
			#if not self.start_approval(cr, uid, id):
				#return False
				
			self.write(cr, uid, [id], {'state':'waiting'})
		return True	
		
	def workflow_action_ready(self, cr, uid, ids, context={}):
		"""
		Method yang dijalankan ketika ready
		
		* Merubah state
		"""
		for id in ids:
				
			self.write(cr, uid, [id], {'state':'ready'})
		return True			
	
	def workflow_action_proforma(self, cr, uid, ids, context={}):
		"""
		Method yang dijalankan ketika confirm
		
		* Merubah state
		* Memberikan nomor pada voucher
		"""	
		for id in ids:
			if not self.proforma_voucher(cr, uid, [id]):
				return False
				
			self.write(cr, uid, [id], {'state':'proforma'})
		return True		
	
	def workflow_action_posted(self, cr, uid, ids, context={}):
		"""
		Method yang dijalankan ketika confirm
		
		* Merubah state
		* Memberikan nomor pada voucher jika belum ada nomor
		* Membuat penjurnalan
		"""	
		for id in ids:				
			if not self.post_journal_entry(cr, uid, id):
				return False
						
			self.write(cr, uid, [id], {'state':'posted'})
		return True		
	
	def workflow_action_cancel(self, cr, uid, ids, context={}):
		"""
		Method yang dijalankan ketika cancel
		
		* Merubah state
		"""	
		for id in ids:
			#TODO
			if not self.cancel_account_voucher(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state':'cancel'})
		return True		
		
	def button_workflow_action_confirm(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
		
			#if not self.check_total_voucher(cr, uid, id):
				#raise osv.except_osv('Warning!', 'Total voucher is not equal with line total')
				#return False		
				
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_confirm', cr)
			

		return True		
		
	def button_workflow_action_waiting(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_waiting', cr)
			
		return True			
		
	def button_workflow_action_proforma(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_proforma', cr)
			
		return True		
		
	def button_workflow_action_posted(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_posted', cr)
			
		return True		
		
	def button_workflow_action_cancel(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_cancel', cr)
			
		return True		
		
	def button_workflow_action_ready(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_ready', cr)
			
		return True						

	def post_journal_entry(self, cr, uid, id):
		obj_move = self.pool.get('account.move')
		 
		voucher = self.browse(cr, uid, [id])[0]
		
		if not voucher.move_id:
			if not self.proforma_voucher(cr, uid, [id]):
				return False
		
		voucher = self.browse(cr, uid, [id])[0]
		obj_move.post(cr, uid, [voucher.move_id.id], context={})			
		
		return True
		
	def button_cancel(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.cancel_account_voucher(cr, uid, id):
				return False
				
			if not self.cancel_workflow_instance(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state' : 'cancel'})
		return True		
		
	def cancel_account_voucher(self, cr, uid, id, context=None):

		obj_reconcile = self.pool.get('account.move.reconcile')
		obj_move = self.pool.get('account.move')
		obj_move_line = self.pool.get('account.move.line')
	
		voucher = self.browse(cr, uid, [id], context)[0]
	
		# Batalkan rekonsiliasi setiap voucher line
		for line in voucher.move_ids:
		    if line.reconcile_id:
		        move_lines = [move_line.id for move_line in line.reconcile_id.line_id]
		        move_lines.remove(line.id)
		        obj_reconcile(cr, uid, line.reconcile_id.id)
		        if len(move_lines) >= 2:
		            obj_move_line.reconcile_partial(cr, uid, move_lines, 'auto',context=context)
		            
		# Hapus account.move
		if voucher.move_id:
		    obj_move.button_cancel(cr, uid, [voucher.move_id.id])
		    obj_move.unlink(cr, uid, [voucher.move_id.id])
		    
		res = 	{
					'move_id' : False,
					}
				
		self.write(cr, uid, [id], res)
	
		return True
		
	def cancel_workflow_instance(self, cr, uid, id):
		wkf_service = netsvc.LocalService('workflow')

		wkf_service.trg_delete(uid, 'account.voucher', id, cr)
		wkf_service.trg_create(uid, 'account.voucher', id, cr)
		wkf_service.trg_validate(uid, 'account.voucher', id, 'button_cancel', cr)

		return True			
		
	def button_set_to_draft(self, cr, uid, ids, context={}):
		"""
		Method yang dijalankan ketika user menekan tombol set to draft
		"""
		
		for id in ids:
			if not self.set_to_draft(cr, uid, id, context):
				return False
				
		return True
		
	def set_to_draft(self, cr, uid, id, context={}):
		"""
		Method yang dijalankan untuk merubah cancel -> draft
		"""
		wkf_service = netsvc.LocalService('workflow')
		
		voucher = self.browse(cr, uid, [id], context)[0]
		
		wkf_service.trg_delete(uid, 'account.voucher', id, cr)
		wkf_service.trg_create(uid, 'account.voucher', id, cr)
		
		self.write(cr, uid, [id], {'state':'draft'})
		
		return True					
		
		
	def check_total_voucher(self, cr, uid, id):
		"""
		Method untuk melakukan pengecekan agar total voucher == sum amount semua voucher line
		"""
		
		voucher = self.browse(cr, uid, [id])[0]
		
		total = 0.0
		if voucher.line_ids:
			for line in voucher.line_ids:
				total += line.amount
				
		if voucher.amount == total and voucher.voucher_type_id.check_total:
			return True
		elif voucher.amount != total and voucher.voucher_type_id.check_total:
			return False
		else:
			return True
			
	def proforma_voucher(self, cr, uid, ids, context=None):
		"""
		Override
		"""
		
		for id in ids:
			pass
			#if not self.check_total_voucher(cr, uid, id):
				#raise osv.except_osv('Warning!', 'Total voucher is not equal with line total')
				#return False

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
			#raise osv.except_osv('a',str(ml_writeoff))
			if ml_writeoff:
				move_line_pool.create(cr, uid, ml_writeoff, context)
			# We post the voucher.
			self.write(cr, uid, [voucher.id], {
				'move_id': move_id,
				'number': name,
			})

			# We automatically reconcile the account move lines.
			for rec_ids in rec_list_ids:
				if len(rec_ids) >= 2:
				    move_line_pool.reconcile_partial(cr, uid, rec_ids, writeoff_acc_id=False, writeoff_period_id=False, writeoff_journal_id=False)
		return True
		
	def voucher_move_line_create(self, cr, uid, voucher_id, line_total, move_id, company_currency, current_currency, context=None):
		'''
		Create one account move line, on the given account move, per voucher line where amount is not 0.0.
		It returns Tuple with tot_line what is total of difference between debit and credit and
		a list of lists with ids to be reconciled with this format (total_deb_cred,list_of_lists).

		:param voucher_id: Voucher id what we are working with
		:param line_total: Amount of the first line, which correspond to the amount we should totally split among all voucher lines.
		:param move_id: Account move wher those lines will be joined.
		:param company_currency: id of currency of the company to which the voucher belong
		:param current_currency: id of currency of the voucher
		:return: Tuple build as (remaining amount not allocated on voucher lines, list of account_move_line created in this method)
		:rtype: tuple(float, list of int)
		'''
		if context is None:
		    context = {}
		move_line_obj = self.pool.get('account.move.line')
		currency_obj = self.pool.get('res.currency')
		tax_obj = self.pool.get('account.tax')
		tot_line = line_total
		rec_lst_ids = []

		voucher_brw = self.pool.get('account.voucher').browse(cr, uid, voucher_id, context)
		ctx = context.copy()
		ctx.update({'date': voucher_brw.date})
		for line in voucher_brw.line_ids:
		    #create one move line per voucher line where amount is not 0.0
		    if not line.amount:
		        continue
		    # convert the amount set on the voucher line into the currency of the voucher's company
		    amount = self._convert_amount(cr, uid, line.untax_amount or line.amount, voucher_brw.id, context=ctx)
		    # if the amount encoded in voucher is equal to the amount unreconciled, we need to compute the
		    # currency rate difference
		    if line.amount == line.amount_unreconciled:
		        currency_rate_difference = line.move_line_id.amount_residual - amount
		    else:
		        currency_rate_difference = 0.0
		    move_line = {
		        'journal_id': voucher_brw.journal_id.id,
		        'period_id': voucher_brw.period_id.id,
		        'name': line.name or '/',
		        'account_id': line.account_id.id,
		        'move_id': move_id,
		        'partner_id': voucher_brw.partner_id.id,
		        'currency_id': line.move_line_id and (company_currency <> line.move_line_id.currency_id.id and line.move_line_id.currency_id.id) or False,
		        'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
		        'analytics_id' : line.analytics_id and line.analytics_id.id or False,
		        'quantity': 1,
		        'credit': 0.0,
		        'debit': 0.0,
		        'date': voucher_brw.date
		    }
		    if amount < 0:
		        amount = -amount
		        if line.type == 'dr':
		            line.type = 'cr'
		        else:
		            line.type = 'dr'

		    if (line.type=='dr'):
		        tot_line += amount
		        move_line['debit'] = amount
		    else:
		        tot_line -= amount
		        move_line['credit'] = amount

		    if voucher_brw.tax_id and voucher_brw.type in ('sale', 'purchase'):
		        move_line.update({
		            'account_tax_id': voucher_brw.tax_id.id,
		        })

		    if move_line.get('account_tax_id', False):
		        tax_data = tax_obj.browse(cr, uid, [move_line['account_tax_id']], context=context)[0]
		        if not (tax_data.base_code_id and tax_data.tax_code_id):
		            raise osv.except_osv(_('No Account Base Code and Account Tax Code!'),_("You have to configure account base code and account tax code on the '%s' tax!") % (tax_data.name))

		    # compute the amount in foreign currency
		    foreign_currency_diff = 0.0
		    amount_currency = False
		    if line.move_line_id:
		        voucher_currency = voucher_brw.currency_id and voucher_brw.currency_id.id or voucher_brw.journal_id.company_id.currency_id.id
		        # We want to set it on the account move line as soon as the original line had a foreign currency
		        if line.move_line_id.currency_id and line.move_line_id.currency_id.id != company_currency:
		            # we compute the amount in that foreign currency. 
		            if line.move_line_id.currency_id.id == current_currency:
		                # if the voucher and the voucher line share the same currency, there is no computation to do
		                sign = (move_line['debit'] - move_line['credit']) < 0 and -1 or 1
		                amount_currency = sign * (line.amount)
		            elif line.move_line_id.currency_id.id == voucher_brw.payment_rate_currency_id.id:
		                # if the rate is specified on the voucher, we must use it
		                voucher_rate = currency_obj.browse(cr, uid, voucher_currency, context=ctx).rate
		                amount_currency = (move_line['debit'] - move_line['credit']) * voucher_brw.payment_rate * voucher_rate
		            else:
		                # otherwise we use the rates of the system (giving the voucher date in the context)
		                amount_currency = currency_obj.compute(cr, uid, company_currency, line.move_line_id.currency_id.id, move_line['debit']-move_line['credit'], context=ctx)
		        if line.amount == line.amount_unreconciled and line.move_line_id.currency_id.id == voucher_currency:
		            sign = voucher_brw.type in ('payment', 'purchase') and -1 or 1
		            foreign_currency_diff = sign * line.move_line_id.amount_residual_currency + amount_currency

		    move_line['amount_currency'] = amount_currency
		    voucher_line = move_line_obj.create(cr, uid, move_line)
		    rec_ids = [voucher_line, line.move_line_id.id]

		    if not currency_obj.is_zero(cr, uid, voucher_brw.company_id.currency_id, currency_rate_difference):
		        # Change difference entry in company currency
		        exch_lines = self._get_exchange_lines(cr, uid, line, move_id, currency_rate_difference, company_currency, current_currency, context=context)
		        new_id = move_line_obj.create(cr, uid, exch_lines[0],context)
		        move_line_obj.create(cr, uid, exch_lines[1], context)
		        rec_ids.append(new_id)

		    if line.move_line_id and line.move_line_id.currency_id and not currency_obj.is_zero(cr, uid, line.move_line_id.currency_id, foreign_currency_diff):
		        # Change difference entry in voucher currency
		        move_line_foreign_currency = {
		            'journal_id': line.voucher_id.journal_id.id,
		            'period_id': line.voucher_id.period_id.id,
		            'name': _('change')+': '+(line.name or '/'),
		            'account_id': line.account_id.id,
		            'move_id': move_id,
		            'partner_id': line.voucher_id.partner_id.id,
		            'currency_id': line.move_line_id.currency_id.id,
		            'amount_currency': -1 * foreign_currency_diff,
		            'quantity': 1,
		            'credit': 0.0,
		            'debit': 0.0,
		            'date': line.voucher_id.date,
		        }
		        new_id = move_line_obj.create(cr, uid, move_line_foreign_currency, context=context)
		        rec_ids.append(new_id)

		    if line.move_line_id.id:
		        rec_lst_ids.append(rec_ids)

		return (tot_line, rec_lst_ids)			
		
		
        
        
							
account_voucher()							
	
