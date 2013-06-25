# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from lxml import etree

import netsvc
import time

from osv import osv,fields
from tools.translate import _
import decimal_precision as dp
from datetime import datetime, date

class wizard_print_trial_balance(osv.osv_memory):
    _name = 'account.wizard_print_trial_balance'
    _description = 'Wizard Print Trial Balance'
    
    _columns = {
                            'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
                            'to_date' : fields.date(string='To Date', required=True),
                            }
                            
    def button_print_report(self, cr, uid, ids, data, context=None):
		obj_user = self.pool.get('res.users')
		if context is None:
			context = {}
			
			
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.account_root_id:
			raise osv.except_osv('Peringatan!', 'Akun root aset belum ditentukan')
			
		data = {}
		wizard = self.browse(cr, uid, ids, context)[0]
		res =	{
		            'to_date' : wizard.to_date,
		            }
				
		data['form'] = res
		
		return	{
				'type': 'ir.actions.report.xml',
				'report_name': 'report_trial_balance',
				'datas': data,
				}

        
        
                            

        
wizard_print_trial_balance()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

