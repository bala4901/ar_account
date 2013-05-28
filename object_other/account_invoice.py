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
	
	def get_amount_to_text(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		amount_to_text = []
		obj_account_voucher = self.pool.get('account.voucher')
		obj_res_currency = self.pool.get('res.currency')

		for account_voucher in obj_account_voucher.browse(cr, uid, ids):
			amount_to_text = obj_res_currency.terbilang(cr, uid, account_voucher.currency_id.id, account_voucher.amount) # INI CONTOH TERBILANG NYA
			#raise osv.except_osv(_('Test !'), _('%s')%amount_to_text)
			res[account_voucher.id] = amount_to_text
		return res

	_columns =	{
                                'amount_to_text' : fields.function(fnct=get_amount_to_text, string='Terbilang', type='text', method=True, store=True),
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
					
      
		
			

		
account_invoice()




