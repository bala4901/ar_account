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
import netsvc

class other_bank_receipt(osv.osv):
	_name = 'account.other_bank_receipt'
	_inherit = 'account.voucher'
	_table = 'account_voucher'
	_description = 'Other Bank Receipt'
	_order = 'name'
	
	def check_access_rights(self, cr, uid, operation, raise_exception=True):
		"""
		override in order to redirect the check of access rights on the account.voucher object
		"""
		return self.pool.get('account.voucher').check_access_rights(cr, uid, operation, raise_exception=raise_exception)
		
	def check_access_rule(self, cr, uid, ids, operation, context=None):
		"""
		override in order to redirect the check of access rules on the account.voucher object
		"""
		return self.pool.get('account.voucher').check_access_rule(cr, uid, ids, operation, context=context)
		
	def create(self, cr, uid, value, context=None):
		"""
		override method orm create
		"""
		new_id = super(other_bank_receipt, self).create(cr, uid, value, context)
		
		wkf_service = netsvc.LocalService('workflow')
		wkf_service.trg_create(uid, 'account.voucher', new_id, cr)
		
		return new_id
		
	def unlink(self, cr, uid, ids, context=None):
		"""
		override method orm
		"""
		wkf_service = netsvc.LocalService('workflow')
		for id in ids:
			wkf_service.trg_delete(uid, 'account.voucher', id, cr)
			
		return super(other_bank_receipt, self).unlink(cr, uid, ids, context)
		
	def button_proforma_voucher(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'proforma_voucher', cr)
			
		return True
		
	def button_cancel_voucher(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'cancel_voucher', cr)
			
		return True	
		


other_bank_receipt()



