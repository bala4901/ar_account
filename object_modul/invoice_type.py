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


class invoice_type(osv.osv):
	_name = 'account.invoice_type'
	_description = 'Invoice Type'
	
		
	def default_active(self, cr, uid, context={}):
		return True		
		
	def default_invoice_type(self, cr, uid, context={}):
		return 'out_invoice'

	_columns =	{
							'kode' : fields.char(string='Code', size=100, required=True),
							'name' : fields.char(string='Name', size=100, required=True),
							'active' : fields.boolean(string='Active'),
							'default_invoice_type' : fields.selection(selection=[('out_invoice','Customer Invoice'),('in_invoice','Supplier Invoice'),('out_refund','Customer Refund'),('in_refund','Supplier Refund')], string='Default Invoice Type', required=True),
							'description' : fields.text(string='Description'),
							'line_ids' : fields.one2many(string='Invoice Type Line', obj='account.invoice_type_line', fields_id='invoice_type_id'),
							'refund_invoice_type_id'  : fields.property('account.invoice_type', string='Refund Invoice Type', type='many2one', view_load=True, relation='account.invoice_type'),
							'account_journal_id'  : fields.property('account.journal', string='Account Journal', type='many2one', view_load=True, relation='account.journal'),
							}
				
	_defaults =	{
							'active' : default_active,
							}

invoice_type()

class invoice_type_line(osv.osv):
	_name = 'account.invoice_type_line'
	_description = 'Invoice Type Line'
	
	_columns =	{
							'invoice_type_id' : fields.many2one(string='Invoice Type', obj='account.invoice_type'),
							'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
							'journal_id' : fields.many2one(string='Journal', obj='account.journal', required=True),
							}
	
invoice_type_line()
	




