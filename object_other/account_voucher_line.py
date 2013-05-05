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

							
account_voucher_line()							
	
