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
from tools.translate import _

class account_move(osv.osv):
	_name = 'account.move'
	_inherit = 'account.move'
	
	def default_journal_id(self, cr, uid, context={}):
		obj_account_journal = self.pool.get('account.journal')
		
		if not context:
			context = {}

		account_journal = context.get('account_journal', False)
		account_journal_id = False
		if account_journal:			
			account_journal_ids = obj_account_journal.search(cr, uid, [('name','=',account_journal)])
			if account_journal_ids : account_journal_id = account_journal_ids[0]
	
		return account_journal_id
		
	_defaults =	{
							'journal_id' : default_journal_id,
							}

	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_move, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_move, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(account_move, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
account_move()



