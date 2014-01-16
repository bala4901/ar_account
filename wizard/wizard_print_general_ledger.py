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
        return {}
        
        
                            

        
wizard_print_general_ledger()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

