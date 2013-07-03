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

class wizard_print_cash_flow(osv.osv_memory):
    _name = 'account.wizard_print_cash_flow'
    _description = 'Wizard Print Cash Flow'
    
    _columns = {
                            'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
                            'to_date' : fields.date(string='To Date', required=True),
                            }
                            
    def button_print_report(self, cr, uid, ids, data, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        obj_account = self.pool.get('account.account')
        obj_period = self.pool.get('account.period')

        
        period_ids = obj_period.find(cr, uid, wizard.to_date)
        
        if not period_ids:
            raise osv.except_osv('Warning!', 'Please define period for start date')
            
        period = obj_period.browse(cr, uid, period_ids)[0]
        
        from_date = period.fiscalyear_id.date_start
        to_date = wizard.to_date  
        
        data['ids'] = self.pool.get('account.account').search(cr, uid, [])
        data['model'] = 'account.account'
        data['output_type'] = 'pdf'
        val =   {
                    'to_date' : '%s 00:00:00' % (wizard.to_date),
                    }
        data['variables'] = val
        return {'type': 'ir.actions.report.xml', 'report_name': 'account.report_cash_flow', 'datas': data, 'context' : {'date_from' : from_date, 'date_to' : to_date}}

        
        
                            

        
wizard_print_cash_flow()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

