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

class account_voucher(osv.osv):
        _name = 'account.voucher'
	_inherit = 'account.voucher'
	
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
	
	_columns =	{
                        'voucher_type_id' : fields.many2one(obj='account.voucher_type', string='Voucher Type'),
                        'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')]),
                        'cheque_number' : fields.char(string='Cheque Number', size=50),
                        'cheque_date' : fields.date(string='Cheque Date'),
                        'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account'),
                        'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=True, readonly=True),
                        'cheque_recepient' : fields.char(string='Cheque Recepient', size=100),
                        'cheque_is_giro' : fields.boolean('Is Giro?')
                        }
    
	_defaults =	{
                        'voucher_type_id' : default_voucher_type_id,
                        'type' : default_type,
                        }
							
account_voucher()							
	
