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

class wizard_print_general_ledger(osv.osv_memory):
    _name = 'account.wizard_print_general_ledger'
    _description = 'Wizard Print General Ledger'
    
    _columns = {
                            'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
                            'account_id' : fields.many2one(string='Account', obj='account.account', required=True, domain=[('type','!=','view'),('type','!=','consollidation'),('type','!=','closed')]),
                            'from_date' : fields.date(string='From Date', required=True),
                            'to_date' : fields.date(string='To Date', required=True),
                            }
                            
    def button_print_report(self, cr, uid, ids, data, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        obj_account = self.pool.get('account.account')
        obj_period = self.pool.get('account.period')
        from_date = date(int(wizard.from_date[0:4]), int(wizard.from_date[5:7]),int(wizard.from_date[8:10]))
        #raise osv.except_osv('a', str(from_date))
        first_date_ordinal = datetime.toordinal(from_date) - 1
        first_date = date.fromordinal(first_date_ordinal).strftime('%Y-%m-%d')
        #raise osv.except_osv('a', first_date)
        
        period_ids = obj_period.find(cr, uid, first_date)
        
        if not period_ids:
            raise osv.except_osv('Warning!', 'Please define period for start date')
            
        period = obj_period.browse(cr, uid, period_ids)[0]
        
        date_begin = period.fiscalyear_id.date_start
        
        
        
        
        
        
        
        account = obj_account.browse(cr, uid, [wizard.account_id.id], context={'date_to' : first_date, 'date_from' : date_begin})[0]
        kriteria = [('account_id','=',wizard.account_id.id),('date','>=',wizard.from_date),('date','<=',wizard.to_date),('state','=','valid'),('move_id.state','=','posted')]
        data['ids'] = self.pool.get('account.move.line').search(cr, uid, kriteria, order='date asc')
        data['model'] = 'account.move.line'
        data['output_type'] = 'pdf'
        val =   {
                    'from_date' : '%s 00:00:00' % (wizard.from_date),
                    'to_date' : '%s 23:59:00' % (wizard.to_date),
                    'account_name' : wizard.account_id.name,
                    'init_bal' : account.balance,
                    }
        data['variables'] = val
        #raise osv.except_osv('a', str(account.balance))
        return {'type': 'ir.actions.report.xml', 'report_name': 'account.report_general_ledger', 'datas': data, 'context' : {'pentaho_defaults' : {'from_date' : wizard.from_date}}}

        
        
                            

        
wizard_print_general_ledger()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

