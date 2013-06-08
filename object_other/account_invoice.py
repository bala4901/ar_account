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


import time
from operator import itemgetter

import netsvc
from osv import fields, osv
from osv.orm import except_orm
import pooler
from tools import config
from tools.translate import _

class account_invoice(osv.osv):
	_name = 'account.invoice'
	_inherit = 'account.invoice'
	
	def default_journal_id(self, cr, uid, context={}):
		"""
		Method untuk mencari nilai default field journal_id
		"""
		
		obj_invoice_type_line = self.pool.get('account.invoice_type_line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		invoice_type_id = self.default_invoice_type_id(cr, uid, context)
		
		if not invoice_type_id : return False
		
		kriteria = [('invoice_type_id','=',invoice_type_id),('company_id','=', user.company_id.id)]
		line_ids = obj_invoice_type_line.search(cr, uid, kriteria)
		
		if not line_ids : return False
		
		line = obj_invoice_type_line.browse(cr, uid, line_ids)[0]
		
		return line.journal_id.id
			
	def default_type(self, cr, uid, context={}):
		obj_journal = self.pool.get('account.journal')
		journal_id = self.default_journal_id(cr, uid, context)
		
		if not journal_id:
			return 'out_invoice'
			
		journal = obj_journal.browse(cr, uid, [journal_id])[0]
		
		if journal.type == 'sale':
			return 'out_invoice'
		elif journal.type == 'purchase':
			return 'in_invoice'
		elif journal.type == 'sale_refund':
			return 'out_refund'
		elif journal.type == 'purchase_refund':
			return 'in_refund'
			
	def default_invoice_type_id(self, cr, uid, context={}):
		obj_invoice_type = self.pool.get('account.invoice_type')
		
		invoice_type_name = context.get('invoice_type', False)
		
		if not invoice_type_name:
			return False
			
		invoice_type_ids = obj_invoice_type.search(cr, uid, [('name','=',invoice_type_name)])
		
		if not invoice_type_ids : return False
		
		return invoice_type_ids[0]
		
	def get_amount_to_text(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		amount_to_text = []
		obj_account_invoice = self.pool.get('account.invoice')
		obj_res_currency = self.pool.get('res.currency')

		for account_invoice in obj_account_invoice.browse(cr, uid, ids):

			#amount_to_text = obj_res_currency.terbilang(cr, uid, account_invoice.currency_id.id, account_invoice.amount_total)
			res[account_invoice.id] = '-' #amount_to_text
		return res		
			

	_columns =	{
								'invoice_type_id' : fields.many2one(string='Invoice Type', obj='account.invoice_type'),
                                'amount_to_text' : fields.function(fnct=get_amount_to_text, string='Terbilang', type='text', method=True, store=True),
			            }
			
	_defaults =	{
							'journal_id' : default_journal_id,
							'type' : default_type,
							'invoice_type_id' : default_invoice_type_id,
							}






		
	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		if context is None:
			context = {}
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_invoice, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context

		if context is None:
			context = {}
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_invoice, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context

		if context is None:
			context = {}
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_invoice, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
	def button_invoice_open(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.invoice', id, 'invoice_open', cr)
			
		return True
		
	def button_invoice_proforma2(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.invoice', id, 'invoice_proforma2', cr)
			
		return True	
		
	def button_invoice_cancel(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.invoice', id, 'invoice_cancel', cr)
			
		return True		
		
			
					
      
		
			

		
account_invoice()




