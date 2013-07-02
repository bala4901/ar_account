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

import xml
import copy
from operator import itemgetter
import time
import datetime
from report import report_sxw
import locale

class report_equity_change(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_equity_change, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
			'locale':locale,            
        })
        self.context = context
        
    def set_context(self, objects, data, ids, report_type=None):
        obj_period = self.pool.get('account.period')
        self.to_date = data['form']['to_date']        
        
        period_ids = obj_period.find(self.cr, self.uid, self.to_date)
        
        if not period_ids:
            return super(report_equity_change, self).set_context(objects, data, ids, report_type=report_type)           
            
        period = obj_period.browse(self.cr, self.uid, period_ids)[0]
        
        self.from_date =  period.fiscalyear_id.date_start        

        return super(report_equity_change, self).set_context(objects, data, ids, report_type=report_type)           

        

        

report_sxw.report_sxw('report.report_equity_change', 'account.account', 'addons/ar_account/report/equity_change.rml', parser=report_equity_change, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
