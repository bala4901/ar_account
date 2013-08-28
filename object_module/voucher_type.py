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

DEFAULT_HEADER_TYPE = [
    ('sale', 'Sale'),
    ('purchase', 'Purchase'),
    ('payment', 'Payment'),
    ('receipt', 'Receipt'),
]

DEFAULT_DETAIL_TYPE_SELECTION = [
    ('dr', 'Debit'),
    ('cr', 'Credit'),
]

class voucher_type(osv.osv):
	_name = 'account.voucher_type'
	_description = 'Voucher Type'
	
	def default_check_total(self, cr, uid, context={}):
		return True
		
	def default_active(self, cr, uid, context={}):
		return True		

	_columns =	{
					'kode' : fields.char(string='# Kode', size=100, required=True),
					'name' : fields.char(string='Name', size=100, required=True),
					'active' : fields.boolean(string='Active'),
					'description' : fields.text(string='Description'),
					'default_header_type' : fields.selection(selection=DEFAULT_HEADER_TYPE, string='Default Header Type'),
					'default_detail_type_selection' : fields.selection(selection=DEFAULT_DETAIL_TYPE_SELECTION, string='Default Detail Type Selection'),
					'allowed_journal_ids' : fields.many2many(obj='account.journal', rel='account_voucher_type_account_journal_rel', id1='voucher_type_id', id2='account_journal_id'),	
					'model_name' : fields.char(string='Model Name', size=100),
					'model_view_form' : fields.char(string='Model View Form', size=100),		
					'modul_origin' : fields.char(string='Modul Origin', size=100),	
					'check_total' : fields.boolean(string='Check For Total'),
				}
				
	_defaults =	{
							'active' : default_active,
							'check_total' : default_check_total,
							}

voucher_type()




